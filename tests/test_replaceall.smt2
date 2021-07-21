(set-logic QF_SLIA)
(set-option :strings-exp true)

(declare-fun x () String)
(declare-fun y () String)
(assert (str.contains (str.replace_all x "AB" y) "a"))

(check-sat)
(get-model)