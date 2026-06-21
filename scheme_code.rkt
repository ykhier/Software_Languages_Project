#lang racket

(require racket/list
         racket/string
         racket/math
         racket/runtime-path)

(define (isFinite v)
  (if (nan? v)
      #f
      (if (infinite? v)
          #f
          #t)))

(define (horner-eval coeffs x)
  (let loop ([acc (car coeffs)] [rest (cdr coeffs)])
    (if (null? rest)
        acc
        (loop (+ (* acc x) (car rest)) (cdr rest)))))

(define (horner-eval-with-deriv coeffs x)
  (let loop ([res (car coeffs)] [der 0.0] [rest (cdr coeffs)])
    (if (null? rest)
        (values res der)
        (let* ([c (car rest)] [new-der (+ (* der x) res)] [new-res (+ (* res x) c)])
          (loop new-res new-der (cdr rest))))))

(define (derivative-coefficients coeffs)
  (let loop ([rest coeffs] [power (- (length coeffs) 1)] [acc '()])
    (if (or (null? rest) (= power 0))
        (reverse acc)
        (loop (cdr rest) (- power 1) (cons (* (car rest) power) acc)))))

(define (find-finite-edge coeffs start other)
  (let ([f (horner-eval coeffs start)])
    (if (isFinite f)
        (values start f)
        (let loop ([a start] [k 0])
          (if (>= k 100)
              (values #f #f)
              (let* ([a2 (/ (+ a other) 2.0)] [f2 (horner-eval coeffs a2)])
                (if (isFinite f2)
                    (values a2 f2)
                    (loop a2 (+ k 1)))))))))

(define (safe-bracket coeffs a b)
  (let-values ([(left f-left) (find-finite-edge coeffs a b)])
    (if (not left)
        #f
        (let-values ([(right f-right) (find-finite-edge coeffs b left)])
          (if (not right)
              #f
              (list left right f-left f-right))))))

(define (newton-raphson coeffs x0 eps)
  (let loop ([x x0] [k 0])
    (if (>= k 100)
        #f
        (let-values ([(fx dfx) (horner-eval-with-deriv coeffs x)])
          (cond
            [(or (not (isFinite fx)) (not (isFinite dfx)) (= dfx 0)) #f]
            [(< (abs fx) eps) x]
            [else
             (let ([xnew (- x (/ fx dfx))])
               (cond
                 [(not (isFinite xnew)) #f]
                 [(< (abs (- xnew x)) eps) xnew]
                 [else (loop xnew (+ k 1))]))])))))

(define (bisection coeffs a b eps)
  (let loop ([a a] [b b] [fa (horner-eval coeffs a)])
    (if (> (/ (- b a) 2.0) eps)
        (let* ([mid (/ (+ a b) 2.0)]
               [fmid (horner-eval coeffs mid)])
          (cond
            [(= fmid 0) mid]
            [(< (* fa fmid) 0) (loop a mid fa)]
            [else (loop mid b fmid)]))
        (/ (+ a b) 2.0))))

(define (first-degree c0 c1)
  (list (/ (- c1) c0)))

(define (second-degree a b c)
  (let ([disc (- (* b b) (* 4.0 a c))])
    (if (< disc 0)
        '()
        (let ([sq (sqrt disc)])
          (list (/ (- (- b) sq) (* 2.0 a)) (/ (+ (- b) sq) (* 2.0 a)))))))

(define (build-chain coeffs)
  (reverse
   (let loop ([current coeffs] [acc (list coeffs)])
     (if (> (length current) 3)
         (let ([d (derivative-coefficients current)])
           (loop d (cons d acc))) acc))))

(define (roots-in-range roots a b)
  (let loop ([rs roots] [acc '()])
    (cond
      [(null? rs) (reverse acc)]
      [(and (<= a (car rs)) (<= (car rs) b))
       (loop (cdr rs) (cons (car rs) acc))]
      [else (loop (cdr rs) acc)])))

(define (refine-level poly roots a b eps)
  (let* ([dcoeffsRoots (roots-in-range roots a b)] [splitPoints (append (list a) dcoeffsRoots (list b))])
    (let loop ([pts splitPoints] [acc '()])
      (if (or (null? pts) (null? (cdr pts)))
          (reverse acc)
          (let* ([lo (car pts)] [hi (cadr pts)] [finiteBracket (safe-bracket poly lo hi)])
            (if (not finiteBracket)
                (loop (cdr pts) acc)
                (let ([lo (first finiteBracket)] [hi (second finiteBracket)] [fa (third finiteBracket)] [fb (fourth finiteBracket)])
                  (if (<= (* fa fb) 0)
                      (let* ([x0 (/ (+ lo hi) 2.0)]
                             [root (or (newton-raphson poly x0 eps) (bisection poly lo hi eps))])
                        (if (and (isFinite root) (<= a root) (<= root b))
                            (loop (cdr pts) (cons root acc))
                            (loop (cdr pts) acc)))
                      (loop (cdr pts) acc)))))))))

(define (find-roots coeffs a b eps)
  (let ([deg (- (length coeffs) 1)])
    (cond
      [(<= deg 0) '()]
      [(= deg 1) (first-degree (list-ref coeffs 0) (list-ref coeffs 1))]
      [(= deg 2) (second-degree (list-ref coeffs 0) (list-ref coeffs 1) (list-ref coeffs 2))]
      [else
       (let* ([chain (build-chain coeffs)] [lowest (last chain)] 
              [init-roots (second-degree (list-ref lowest 0) (list-ref lowest 1) (list-ref lowest 2))]
              [process-list (cdr (reverse chain))])

         (let loop ([polys process-list] [roots init-roots])
           (if (null? polys)
               roots
               (loop (cdr polys) (refine-level (car polys) roots a b eps)))))])))

(define (round6 r)
  (/ (round (* r 1000000.0)) 1000000.0))

(define (map-outer-roots bounds)
  (let loop ([ys bounds] [acc '()])
    (cond
      [(null? ys) (reverse acc)]
      [(> (abs (car ys)) 1e-12)
       (loop (cdr ys) (cons (/ 1.0 (car ys)) acc))]
      [else (loop (cdr ys) acc)])))

(define (round-all roots)
  (let loop ([rs roots] [acc '()])
    (if (null? rs)
        (reverse acc)
        (loop (cdr rs) (cons (round6 (car rs)) acc)))))

(define (scan-page coeffs eps)
  (let* ([reversed-coeffs (reverse coeffs)]
         [inner-roots (find-roots coeffs -1.0 1.0 eps)]
         [outer-bounds (find-roots reversed-coeffs -1.0 1.0 eps)]
         [outer-roots (map-outer-roots outer-bounds)]
         [all-roots (append inner-roots outer-roots)])
    (sort (round-all all-roots) <)))

(define (load-coeffs path)
  (with-input-from-file path
    (lambda ()
      (let loop ([acc '()])
        (let ([line (read-line)])
          (if (eof-object? line)
              (reverse acc)
              (let ([trimmed (string-trim line)])
                (if (non-empty-string? trimmed)
                    (loop (cons (exact->inexact (string->number trimmed)) acc))
                    (loop acc)))))))))

(define-runtime-path csv-path "data/poly_coeff_newton.csv")

(define (main)
  (printf "--- Custom Algorithm (CSV file): ---\n")
  (define coeffs (load-coeffs csv-path))
  (define t0 (current-inexact-milliseconds))
  (define roots (scan-page coeffs 1e-12))
  (define elapsed (/ (- (current-inexact-milliseconds) t0) 1000.0))
  (printf "Number of real roots found: ~a\n" (length roots))
  (printf "Roots: ~a\n" roots)
  (printf "Custom Algorithm Runtime: ~a seconds\n" (~r elapsed #:precision 4)))

(module+ main
  (main))
