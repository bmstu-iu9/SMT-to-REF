(set-logic QF_SLIA)
(set-option :strings-exp true)

(declare-fun x () String)
(declare-fun y () String)

(assert (or ( = x (str.replace_all y "AAB" "A")) (not (str.contains x "AA")) ))
(assert (str.contains (str.replace_all x "AB" "") "AB"))

(check-sat)
(get-model)