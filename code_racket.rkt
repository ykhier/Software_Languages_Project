#lang racket

(require racket/list)
(require racket/file)

;; --- 1. טעינת מקדמים ונרמול ---
(define (load-coeffs filename)
  (let* ([lines (file->lines filename)]
         [coeffs (map string->number (map string-trim lines))]
         [max-val (apply max (map abs coeffs))])
    ;; נרמול ראשוני: חלוקת כל איבר במקסימום
    (map (lambda (c) (/ c max-val)) coeffs)))

;; --- 2. שיטת הורנר (ברקורסיית זנב) ---
(define (horner-eval coeffs x)
  (let loop ([lst (cdr coeffs)] [res (car coeffs)])
    (if (null? lst)
        res
        (loop (cdr lst) (+ (* res x) (car lst))))))

;; הערכת הפונקציה והנגזרת במכה אחת
(define (horner-eval-with-deriv coeffs x)
  (let loop ([lst (cdr coeffs)] [res (car coeffs)] [der 0.0])
    (if (null? lst)
        (values res der)
        (loop (cdr lst)
              (+ (* res x) (car lst))
              (+ (* der x) res)))))

;; --- 3. שיטת החצייה (Bisection) ---
(define (bisection coeffs a b eps)
  (let ([fa (horner-eval coeffs a)])
    (let loop ([curr-a a] [curr-b b] [curr-fa fa] [iter 0])
      (if (>= iter 100)
          (/ (+ curr-a curr-b) 2.0)
          (let* ([mid (/ (+ curr-a curr-b) 2.0)]
                 [fmid (horner-eval coeffs mid)])
            (cond
              ;; rational? מחזיר שקר אם המספר הוא אינפיניטי או NaN - דרך בטוחה ב-Scheme
              [(not (rational? fmid)) mid] 
              [(or (< (abs fmid) eps) (< (/ (- curr-b curr-a) 2.0) eps)) mid]
              [(eqv? (sgn fmid) (sgn curr-fa)) (loop mid curr-b fmid (add1 iter))]
              [else (loop curr-a mid curr-fa (add1 iter))]))))))

;; --- 4. שיטת ניוטון-רפסון ---
(define (newton-raphson coeffs x0 eps)
  (let loop ([x x0] [iter 0])
    (if (>= iter 50)
        x
        (let-values ([(fx dfx) (horner-eval-with-deriv coeffs x)])
          (cond
            ;; הגנה מחריגות נומריות
            [(or (not (rational? fx)) (not (rational? dfx)) (< (abs dfx) 1e-15)) x]
            [else
             (let ([x-new (- x (/ fx dfx))])
               (if (< (abs (- x-new x)) eps)
                   x-new
                   (loop x-new (add1 iter))))])))))

;; --- 5. סריקת הטווח (Grid Scan) ---
(define (generate-bounds lo hi step)
  (let ([num-points (add1 (inexact->exact (round (/ (- hi lo) step))))])
    (build-list num-points (lambda (i) (+ lo (* i step))))))

(define (scan-range coeffs lo hi eps)
  (let* ([bounds (generate-bounds lo hi 0.001)]
         [vals (map (lambda (x) (horner-eval coeffs x)) bounds)])
    
    ;; 1. תפיסת שורשים מדויקים שפגעו בול על נקודות הרשת
    (define exact-roots
      (filter-map (lambda (x v) (if (= v 0.0) x #f)) bounds vals))
    
    ;; 2. חיפוש קטעים עם שינוי סימן והפעלת Bisection + Newton
    (define sign-change-roots
      (let loop ([bs bounds] [vs vals] [acc '()])
        (cond
          [(or (null? bs) (null? (cdr bs))) acc]
          [else
           (let ([a (car bs)] [b (cadr bs)]
                 [va (car vs)] [vb (cadr vs)])
             (if (and (rational? va) (rational? vb)
                      (< (* (sgn va) (sgn vb)) 0))
                 (let* ([root-bi (bisection coeffs a b eps)]
                        [root-fn (newton-raphson coeffs root-bi eps)])
                   (loop (cdr bs) (cdr vs) (cons root-fn acc)))
                 (loop (cdr bs) (cdr vs) acc)))])))
    
    ;; איחוד הרשימות
    (append exact-roots (reverse sign-change-roots))))

;; --- 6. הלוגיקה המרכזית (Dual Scan) ---
(define (find-all-roots coeffs eps)
  (let* ([inner-roots (scan-range coeffs -1.05 1.05 eps)]
         [reversed-coeffs (reverse coeffs)]
         [y-roots (scan-range reversed-coeffs -1.05 1.05 eps)]
         
         ;; הפיכת שורשי ה-y חזרה לשורשי x, תוך זריקת שורשים בתוך הרדיוס המרכזי כדי למנוע כפילויות
         [outer-roots (filter-map (lambda (y)
                                    (if (> (abs y) eps)
                                        (let ([x (/ 1.0 y)])
                                          (if (> (abs x) (+ 1.0 eps)) x #f))
                                        #f))
                                  y-roots)]
         
         [all-roots (append inner-roots outer-roots)]
         ;; סינון סופי של חריגות ועיגול ל-6 ספרות לאחר הנקודה
         [valid-roots (filter rational? all-roots)]
         [rounded (map (lambda (x) (/ (round (* x 1000000.0)) 1000000.0)) valid-roots)]
         [sorted (sort rounded <)])
    ;; הסרת כפילויות סופית
    (remove-duplicates sorted =)))

;; --- 7. הרצה ---
(define (main)
  (let* ([file-path "C:\\Users\\shadiBRZ\\Desktop\\colleage\\semester 10\\Software Languages\\poly_coeff_newton.csv"]
         [eps 1e-6])
    ;; תפיסת שגיאות למקרה שהקובץ לא נמצא
    (with-handlers ([exn:fail? (lambda (exn) (printf "Error: ~a\n" (exn-message exn)))])
      (printf "--- Racket Algorithm (Bisection + Newton + Dual Scan) ---\n")
      (let* ([coeffs (load-coeffs file-path)]
             [t0 (current-inexact-milliseconds)]
             [roots (find-all-roots coeffs eps)]
             [t1 (current-inexact-milliseconds)])
        (printf "Number of real roots found: ~a\n" (length roots))
        (printf "Roots: ~a\n" roots)
        (printf "Runtime: ~a seconds\n" (/ (- t1 t0) 1000.0))))))

;; הפעלת התוכנית
(main)