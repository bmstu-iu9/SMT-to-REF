(set-logic QF_SLIA)
(set-option :strings-exp true)

(declare-fun x () String)
(declare-fun y () String)

(assert (and (not (str.contains x "A")) (str.contains x "A") (str.contains x "AB") (str.contains (str.++ x x) "A") (or (not (str.contains x "B")) (not (str.contains x "AB")))))

(check-sat)
(get-model)