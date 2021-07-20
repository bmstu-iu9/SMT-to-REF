(set-logic QF_SLIA)
(set-option :strings-exp true)

(declare-fun x () String)
(declare-fun y () String)

(assert ( = x (str.replace_all y "AAB" "A")))
(assert (str.contains (str.replace_all x "AB" "") "AB"))

(check-sat)
(get-model)