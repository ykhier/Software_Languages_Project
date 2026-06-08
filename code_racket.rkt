#lang racket

(require racket/list)
(require racket/file)
(require racket/math)

(define (load-coeffs filename)
  (let* ([lines (file->lines filename)]
         [coeffs (map string->number (map string-trim lines))]
         [max-val (apply max (map abs coeffs))])
    (map (lambda (c) (/ c max-val)) coeffs)))

(define (horner-eval coeffs x)
  (let loop ([lst (cdr coeffs)] [res (car coeffs)])
    (if (null? lst)
        res
        (loop (cdr lst) (+ (* res x) (car lst))))))

(define (horner-eval-with-deriv coeffs x)
  (let loop ([lst (cdr coeffs)] [res (car coeffs)] [der 0.0])
    (if (null? lst)
        (values res der)
        (loop (cdr lst)
              (+ (* res x) (car lst))
              (+ (* der x) res)))))

(define (bisection coeffs a b eps)
  (let ([fa (horner-eval coeffs a)])
    (let loop ([curr-a a] [curr-b b] [curr-fa fa] [iter 0])
      (if (>= iter 100)
          (/ (+ curr-a curr-b) 2.0)
          (let* ([mid (/ (+ curr-a curr-b) 2.0)]
                 [fmid (horner-eval coeffs mid)])
            (cond
              [(or (< (abs fmid) eps) (< (/ (- curr-b curr-a) 2.0) eps)) mid]
              [(eqv? (sgn fmid) (sgn curr-fa)) (loop mid curr-b fmid (add1 iter))]
              [else (loop curr-a mid curr-fa (add1 iter))]))))))

(define (newton-raphson coeffs x0 eps)
  (let loop ([x x0] [iter 0])
    (if (>= iter 100)
        x
        (let-values ([(fx dfx) (horner-eval-with-deriv coeffs x)])
          (if (< (abs dfx) 1e-15)
              x
              (let ([x-new (- x (/ fx dfx))])
                (if (< (abs (- x-new x)) eps)
                    x-new
                    (loop x-new (add1 iter)))))))))


(define (derivative-coeffs coeffs)
  (let ([n (- (length coeffs) 1)])
    (if (= n 0)
        '(0.0)
        (let loop ([lst coeffs] [power n] [acc '()])
          (if (= power 0)
              (reverse acc)
              (loop (cdr lst)
                    (- power 1)
                    (cons (* (exact->inexact (car lst)) power) acc)))))))

(define (generate-bounds lo hi step)
  (let ([num-points (add1 (inexact->exact (round (/ (- hi lo) step))))])
    (build-list num-points (lambda (i) (+ lo (* i step))))))

(define (build-boundary-indices dvals n)
  (let loop ([i 0] [dvs dvals] [acc (list 0 (- n 1))])
    (if (or (null? dvs) (null? (cdr dvs)))
        (sort (remove-duplicates acc =) <)
        (let ([dv0 (car dvs)]
              [dv1 (car (cdr dvs))])
          (cond
            [(< (* (sgn dv0) (sgn dv1)) 0)
             (loop (add1 i) (cdr dvs) (cons (add1 i) (cons i acc)))]
            [(= dv0 0.0)
             (loop (add1 i) (cdr dvs) (cons i acc))]
            [else
             (loop (add1 i) (cdr dvs) acc)])))))

(define (scan-range coeffs lo hi eps)
  (let* ([bounds (generate-bounds lo hi 0.001)]
         [n (length bounds)]
         [bounds-vec (list->vector bounds)]
         [vals (map (lambda (x) (horner-eval coeffs x)) bounds)]
         [vals-vec (list->vector vals)]
        
         [dcoeffs (derivative-coeffs coeffs)]
         [dvals (map (lambda (x) (horner-eval dcoeffs x)) bounds)]
         [boundary-indices (build-boundary-indices dvals n)])

    (let loop ([idxs boundary-indices] [roots '()])
      (if (null? (cdr idxs))
          (let* ([last-idx (car idxs)]
                 [last-val (vector-ref vals-vec last-idx)]
                 [last-pt (vector-ref bounds-vec last-idx)])
            (if (= last-val 0.0) (cons last-pt roots) roots))
          (let* ([a-idx (car idxs)]
                 [b-idx (cadr idxs)]
                 [fa (vector-ref vals-vec a-idx)]
                 [fb (vector-ref vals-vec b-idx)]
                 [a (vector-ref bounds-vec a-idx)]
                 [b (vector-ref bounds-vec b-idx)]) 
            (cond
              [(= fa 0.0)
               (loop (cdr idxs) (cons a roots))]
              [(< (* (sgn fa) (sgn fb)) 0)
               (let* ([root-bi (bisection coeffs a b eps)]
                      [root-fn (newton-raphson coeffs root-bi eps)])
                 (loop (cdr idxs) (cons root-fn roots)))]
              [else
               (loop (cdr idxs) roots)]))))))

(define (find-all-roots coeffs eps)
  (let* (
         [inner-roots (scan-range coeffs -1.05 1.05 eps)]
         [reversed-coeffs (reverse coeffs)]
         [y-roots (scan-range reversed-coeffs -1.05 1.05 eps)]
         [outer-roots (filter-map (lambda (y)
                                    (if (> (abs y) eps) (/ 1.0 y) #f))
                                  y-roots)]
         [all-roots (append inner-roots outer-roots)]
         [valid-roots (filter rational? all-roots)]
         [rounded (map (lambda (x) (/ (round (* x 1000000.0)) 1000000.0)) valid-roots)]
         [sorted (sort rounded <)])
    (remove-duplicates sorted =)))

(define (main)
  (let* ([file-path (path->string (build-path (current-directory) "data" "poly_coeff_newton.csv"))]
         [eps 1e-6])
    (with-handlers ([exn:fail? (lambda (exn) (printf "Error: ~a\n" (exn-message exn)))])
      (printf "--- Racket Algorithm (Bisection + Newton-Raphson + Dual Scan) ---\n")
      (let* ([coeffs (load-coeffs file-path)]
             [t0 (current-inexact-milliseconds)]
             [roots (find-all-roots coeffs eps)]
             [t1 (current-inexact-milliseconds)])
        (printf "Number of real roots found: ~a\n" (length roots))
        (printf "Roots: ~a\n" roots)
        (printf "Runtime: ~a seconds\n" (/ (- t1 t0) 1000.0))))))
(main)
