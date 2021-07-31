(set-logic QF_SLIA)
(set-option :strings-exp true)
(set-option :produce-models true)

(declare-fun x () String)

(assert (str.contains x "ABAAAC"))
(assert (str.contains x "ABAAAC"))

(check-sat)
(get-model)