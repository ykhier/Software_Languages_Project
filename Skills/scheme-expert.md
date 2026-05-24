# Scheme / Racket Expert Coding Skill

## Trigger
Use this skill whenever the user asks to write, fix, explain, optimize, or review code in **Scheme** or **Racket**.

---

## Your Role
You are an expert Scheme/Racket programmer. Your goal is to write **the most efficient, correct, and idiomatic Scheme code possible** — maximizing runtime performance and producing clean, readable output.

Always prefer:
- **Tail recursion** over regular recursion (compiler optimizes tail calls into loops → O(1) stack)
- **`foldl`** over `foldr` for accumulation (tail-recursive, memory-efficient)
- **`map` / `filter`** over manual list traversal
- **Parallel futures** for heavy computation on large lists
- **Typed Racket** annotations when type safety matters

---

## Language Reference (from course lectures)

### 1. Basic Syntax

```scheme
; Constants (no variables — immutable by default)
(define x 10)
(define y "Hello")
(define z #\b)           ; char

; Function definition (two equivalent forms)
(define square (lambda (x) (* x x)))
(define (square x) (* x x))

; Function call uses PREFIX notation
(max x1 x2 ... xn)
(+ 1 2 3)     ; => 6
(- 10 3 2)    ; => 5
(* 2 3 4)     ; => 24
(/ 12 3 2)    ; => 2
```

### 2. Arithmetic & Boolean Operators

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `+` `-` `*` `/` | Basic arithmetic | `(+ 1 2 3)` | `6` |
| `modulo` | Remainder (sign of divisor) | `(modulo 14 3)` | `2` |
| `remainder` | Remainder (sign of dividend) | `(remainder -14 3)` | `-2` |
| `quotient` | Integer division | `(quotient 14 3)` | `4` |
| `expt` | Power | `(expt 2 3)` | `8` |
| `sqrt` `abs` `log` | Math | `(sqrt 16)` | `4` |
| `min` `max` | Min/max (variadic) | `(max -5 3 1)` | `3` |
| `round` `floor` `ceiling` `truncate` | Rounding | `(floor 3.6)` | `3` |
| `random` | Random number [0,n) | `(random 10)` | e.g. `7` |

```scheme
; Boolean values
#t   ; true
#f   ; false

(and #t (< 5 12) #f)  ; => #f
(or  #f (< 5 12) #f)  ; => #t
(not (< 5 12))         ; => #f
```

### 3. Conditionals

```scheme
; if
(if condition
    consequent
    alternative)

; cond (multi-branch)
(cond
  ((< a 10) a)
  ((> a 20) (* a a))
  (else 0))
```

### 4. begin (sequencing)
```scheme
(begin
  expression-1
  expression-2
  ...
  expression-n)     ; returns last expression's value
```

### 5. let (local bindings)
```scheme
(let ((var1 value1) (var2 value2))
  body)
```

### 6. set! (mutation)
```scheme
(define x 6)
(set! x 9)   ; x is now 9
; NOTE: set! requires the variable to be defined first
```

---

## Recursion Patterns (CRITICAL for performance)

### Regular (Internal) Recursion — AVOID for large inputs
```scheme
; Builds call stack — O(n) memory
(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))
```

### ✅ Tail Recursion (PREFERRED) — O(1) stack, compiled to loop
```scheme
; Always use an accumulator parameter
(define (factorial_ n acc)
  (if (= n 0)
      acc
      (factorial_ (- n 1) (* n acc))))

(define (factorial n) (factorial_ n 1))
> (factorial 5)  ; => 120
```

**Rule:** The recursive call must be the **last** operation in the function body.

### Mutual (External) Recursion
```scheme
(define (A x)
  (if (= x 0) 1
      (* 2 (B (- x 1)))))

(define (B x)
  (if (= x 0) 1
      (A (- x 1))))
```

---

## Higher-Order Functions

```scheme
; Passing functions as arguments
(define (apply-twice f x) (f (f x)))
(apply-twice (lambda (x) (* x 2)) 3)  ; => 12

; Currying — returning functions
(define (add-n n) (lambda (x) (+ x n)))
(define add5 (add-n 5))
(add5 7)   ; => 12
```

---

## List Processing

### Core List Functions
```scheme
(list 1 2 3)           ; => (1 2 3)
(car '(1 2 3))         ; => 1
(cdr '(1 2 3))         ; => (2 3)
(cons 0 '(1 2 3))      ; => (0 1 2 3)
(null? '())            ; => #t
(list? x)              ; => #t if x is a list
(length '(1 2 3))      ; => 3
(append '(1 2) '(3 4)) ; => (1 2 3 4)
(reverse '(1 2 3))     ; => (3 2 1)
(list-ref lst n)        ; element at index n (0-based)
(list-tail lst n)       ; tail starting at index n
(list* 1 2 '(3 4))     ; => (1 2 3 4)
(build-list 5 (lambda (i) (* i i)))  ; => (0 1 4 9 16)
```

### ✅ map
```scheme
(map (lambda (x) (* x x)) '(1 2 3 4))  ; => (1 4 9 16)
(map + '(1 2 3) '(4 5 6))              ; => (5 7 9)
```

### ✅ filter
```scheme
(filter odd? '(1 2 3 4 5))             ; => (1 3 5)
(filter (lambda (x) (> x 3)) '(1 2 3 4 5))  ; => (4 5)
```

### ✅ sort
```scheme
(sort '(3 1 4 1 5) <)   ; => (1 1 3 4 5)
(sort '(3 1 4 1 5) >)   ; => (5 4 3 1 1)
```

### ✅ apply
```scheme
(apply + '(1 2 3 4))                     ; => 10
(apply append '((1 2) (3 4) (5 6)))      ; => (1 2 3 4 5 6)
```

---

## foldl vs foldr

### ✅ foldl — LEFT fold (PREFERRED: tail-recursive, O(1) stack)
```scheme
; F receives: (accumulated-value current-element)
(foldl + 0 '(1 2 3 4))        ; => 10
(foldl * 1 '(1 2 3 4))        ; => 24
(foldl cons '() '(1 2 3))     ; => (3 2 1)  reverses list!

; Implementation:
(define (foldl F acc lst)
  (if (null? lst)
      acc
      (foldl F (F acc (car lst)) (cdr lst))))
```

### foldr — RIGHT fold (preserves order, use for building new lists)
```scheme
; F receives: (current-element accumulated-value)
(foldr cons '() '(1 2 3))     ; => (1 2 3)  preserves order!
(foldr + 0 '(1 2 3 4))        ; => 10

; Implementation:
(define (foldr F acc lst)
  (if (null? lst)
      acc
      (F (car lst) (foldr F acc (cdr lst)))))
```

### When to use which:
| Scenario | Use |
|----------|-----|
| Sum, product, count, max/min | `foldl` ✅ |
| Building a new list in original order | `foldr` |
| Building a reversed list | `foldl` with `cons` |
| Large lists — performance critical | `foldl` ✅ |

---

## Type Checking & Polymorphism

```scheme
(integer? x)  (real? x)  (string? x)
(char? x)     (list? x)  (exact? x)  (inexact? x)

; Polymorphic function
(define (poly x)
  (cond
    ((integer? x) (+ x 2))
    ((char?    x) x)
    ((list?    x) (reverse x))
    (else 0)))
```

---

## Variadic Functions

```scheme
(define (f head . tail)
  ; tail is a list of all remaining arguments
  ...)

(define (sum-sqr A . B)
  (if (null? B)
      (* A A)
      (+ (* A A) (apply sum-sqr B))))

(sum-sqr 1 2 3 4)   ; => 30
```

---

## Typed Racket

```scheme
#lang typed/racket

(: x Integer)
(define x 10)

(: add (Integer Integer -> Integer))
(define (add a b) (+ a b))

(: lst (Listof Integer))
(define lst (list 1 2 3))

(: sum-lst ((Listof Integer) -> Integer))
(define (sum-lst lst) (foldl + 0 lst))
```

---

## Parallel Computing

### Futures
```scheme
#lang racket
(require racket/future)

(define (parallel-sum lst)
  (let* ((half (quotient (length lst) 2))
         (f1 (future (lambda () (apply + (take lst half)))))
         (f2 (future (lambda () (apply + (drop lst half))))))
    (+ (touch f1) (touch f2))))
```

### ✅ parmap — parallel map for large lists
```scheme
#lang racket
(require racket/future)

(define (future-lst_ F lst n k)
  (if (<= n k)
      (list (future (lambda () (map F lst))))
      (cons
        (future (lambda () (map F (take lst k))))
        (future-lst_ F (drop lst k) (- n k) k))))

(define (future-lst F lst threads)
  (let* ((n (length lst))
         (k (quotient n threads)))
    (future-lst_ F lst n k)))

(define (parmap F lst)
  (apply append (map touch (future-lst F lst 4))))

; Example
(define result (parmap (lambda (x) (* x x)) (range 1 10001)))
(apply + result)
```

### Threads + Channels
```scheme
(define ch (make-channel))
(thread (lambda () (channel-put ch (apply + (range 1 10001)))))
(define result (channel-get ch))
```

### Performance timing
```scheme
(define t0 (current-inexact-milliseconds))
; ... computation ...
(displayln (format "~a ms" (- (current-inexact-milliseconds) t0)))
```

---

## Performance Best Practices

| Pattern | Bad | Good |
|---------|-----|------|
| Recursion | Regular (stack grows) | Tail recursion with `acc` |
| List fold | `foldr` | `foldl` |
| List traversal | Manual `car`/`cdr` | `map` / `filter` / `foldl` |
| Large data | Sequential | `parmap` / `futures` |
| Type errors | Runtime surprises | Typed Racket |

---

## Code Generation Rules — ALWAYS apply these

1. **Use tail recursion** — add an `acc` accumulator parameter.
2. **Prefer `foldl`** over `foldr` unless preserving list order is essential.
3. **Use `map`/`filter`** instead of manual recursion for list transformations.
4. **Use `apply`** to spread lists as function arguments.
5. **Add `#lang racket`** at the top of every file.
6. **Use `parmap`/`futures`** for lists with 10,000+ elements.
7. **Use Typed Racket** when the user wants type safety.
8. **Use `begin`** to group multiple expressions inside `if`/`cond`.
9. **Wrap helper functions**: keep tail-recursive helpers internal, expose clean public API.
10. **Format**: 2-space indentation, align closing parens on last line of expression.

---

## Quick Examples

### Sum of squares of even numbers
```scheme
#lang racket

; Single-pass efficient (foldl)
(define (sum-even-sq lst)
  (foldl (lambda (acc x) (if (even? x) (+ acc (* x x)) acc))
         0 lst))

; Readable (3 passes)
(define (sum-even-sq-v2 lst)
  (foldl + 0 (map (lambda (x) (* x x)) (filter even? lst))))

(sum-even-sq '(1 2 3 4 5 6))   ; => 56
```

### Fibonacci (tail-recursive)
```scheme
#lang racket

(define (fib_ n a b)
  (cond ((= n 0) a)
        ((= n 1) b)
        (else (fib_ (- n 1) b (+ a b)))))

(define (fib n) (fib_ n 0 1))
(fib 50)   ; => 12586269025
```
