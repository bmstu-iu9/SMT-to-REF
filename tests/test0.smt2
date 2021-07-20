(set-logic QF_SLIA)
(set-option :strings-exp true)
(set-option :produce-models true)

(declare-fun xvvvvvv112yy () String)

(assert (str.contains xvvvvvv112yy "ABAAAC"))

(check-sat)
(get-model)