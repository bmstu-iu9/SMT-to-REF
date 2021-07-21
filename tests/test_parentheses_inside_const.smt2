(set-logic QF_SLIA)
(set-option :strings-exp true)

(declare-fun x () String)
(declare-fun y () String)

(assert (or (and (str.contains (str.++ x y) "()") (= x (str.++ y "A")) ) (not (or (str.contains y "B") (str.contains (str.++ y x) "AB")))))

(check-sat)
(get-model)