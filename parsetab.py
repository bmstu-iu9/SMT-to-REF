
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND ASSERT BOOL CHECKSAT COLON CONCAT CONST CONTAINS DECLAREFUN EQUALS GETMODEL ID LPAREN NOT OR PRODUCEMODELS QF_S QF_SLIA REPLACEALL RPAREN SETLOGIC SETOPTION STRING STRINGSEXPprogram : logic options decls asserts build\n               | logic decls asserts buildlogic : LPAREN SETLOGIC QF_SLIA RPAREN\n             | LPAREN SETLOGIC QF_S RPARENoptions : option\n               | options optionoption : LPAREN SETOPTION COLON optionname BOOL RPARENoptionname : PRODUCEMODELS\n                  | STRINGSEXPdecls : decl\n             | decls decldecl : LPAREN DECLAREFUN ID LPAREN RPAREN STRING RPARENasserts : assert\n             | asserts assertassert : LPAREN ASSERT expr RPARENexpr : pred\n            | LPAREN AND exprs RPAREN\n            | LPAREN OR exprs RPAREN\n            | LPAREN NOT expr RPARENexprs : expr\n             | exprs exprpred : LPAREN EQUALS str str RPAREN\n            | LPAREN CONTAINS str const RPARENpred : LPAREN CONTAINS str error RPARENstr : IDstr : const\n           | LPAREN CONCAT strs RPARENconst : CONSTstr : LPAREN REPLACEALL str const const RPARENstr : LPAREN REPLACEALL str error const RPAREN\n           | LPAREN REPLACEALL str const error RPAREN\n           | LPAREN REPLACEALL str error error RPARENstrs : str\n            | strs strbuild : LPAREN CHECKSAT RPAREN LPAREN GETMODEL RPAREN'
    
_lr_action_items = {'LPAREN':([0,2,4,5,6,7,10,11,12,13,14,20,22,24,26,27,28,33,38,39,40,41,42,43,44,48,49,50,53,54,55,56,58,61,62,63,64,65,66,70,72,73,75,76,77,78,79,86,87,88,89,],[3,8,8,15,-5,-10,15,-6,23,-11,-13,23,-14,31,37,-3,-4,-16,47,31,31,31,52,52,-15,31,-20,31,52,-25,-26,-28,-7,-17,-21,-18,-19,52,52,-12,52,-33,-22,-23,-24,-27,-34,-29,-31,-32,-30,]),'$end':([1,21,29,71,],[0,-2,-1,-35,]),'SETLOGIC':([3,],[9,]),'SETOPTION':([8,],[16,]),'DECLAREFUN':([8,15,],[17,17,]),'QF_SLIA':([9,],[18,]),'QF_S':([9,],[19,]),'ASSERT':([15,23,],[24,24,]),'COLON':([16,],[25,]),'ID':([17,42,43,53,54,55,56,65,66,72,73,78,79,86,87,88,89,],[26,54,54,54,-25,-26,-28,54,54,54,-33,-27,-34,-29,-31,-32,-30,]),'RPAREN':([18,19,30,32,33,37,45,48,49,50,51,54,55,56,59,60,61,62,63,64,67,68,69,72,73,75,76,77,78,79,82,83,84,85,86,87,88,89,],[27,28,38,44,-16,46,58,61,-20,63,64,-25,-26,-28,70,71,-17,-21,-18,-19,75,76,77,78,-33,-22,-23,-24,-27,-34,86,87,88,89,-29,-31,-32,-30,]),'CHECKSAT':([23,],[30,]),'PRODUCEMODELS':([25,],[35,]),'STRINGSEXP':([25,],[36,]),'AND':([31,],[39,]),'OR':([31,],[40,]),'NOT':([31,],[41,]),'EQUALS':([31,],[42,]),'CONTAINS':([31,],[43,]),'BOOL':([34,35,36,],[45,-8,-9,]),'CONST':([42,43,53,54,55,56,57,65,66,72,73,74,78,79,80,81,86,87,88,89,],[56,56,56,-25,-26,-28,56,56,56,56,-33,56,-27,-34,56,56,-29,-31,-32,-30,]),'STRING':([46,],[59,]),'GETMODEL':([47,],[60,]),'CONCAT':([52,],[65,]),'REPLACEALL':([52,],[66,]),'error':([54,55,56,57,74,78,80,81,86,87,88,89,],[-25,-26,-28,69,81,-27,83,84,-29,-31,-32,-30,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'logic':([0,],[2,]),'options':([2,],[4,]),'decls':([2,4,],[5,10,]),'option':([2,4,],[6,11,]),'decl':([2,4,5,10,],[7,7,13,13,]),'asserts':([5,10,],[12,20,]),'assert':([5,10,12,20,],[14,14,22,22,]),'build':([12,20,],[21,29,]),'expr':([24,39,40,41,48,50,],[32,49,49,51,62,62,]),'pred':([24,39,40,41,48,50,],[33,33,33,33,33,33,]),'optionname':([25,],[34,]),'exprs':([39,40,],[48,50,]),'str':([42,43,53,65,66,72,],[53,57,67,73,74,79,]),'const':([42,43,53,57,65,66,72,74,80,81,],[55,55,55,68,55,55,55,80,82,85,]),'strs':([65,],[72,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> logic options decls asserts build','program',5,'p_program','Parser.py',49),
  ('program -> logic decls asserts build','program',4,'p_program','Parser.py',50),
  ('logic -> LPAREN SETLOGIC QF_SLIA RPAREN','logic',4,'p_logic','Parser.py',55),
  ('logic -> LPAREN SETLOGIC QF_S RPAREN','logic',4,'p_logic','Parser.py',56),
  ('options -> option','options',1,'p_options','Parser.py',61),
  ('options -> options option','options',2,'p_options','Parser.py',62),
  ('option -> LPAREN SETOPTION COLON optionname BOOL RPAREN','option',6,'p_option','Parser.py',67),
  ('optionname -> PRODUCEMODELS','optionname',1,'p_optionname','Parser.py',73),
  ('optionname -> STRINGSEXP','optionname',1,'p_optionname','Parser.py',74),
  ('decls -> decl','decls',1,'p_decls','Parser.py',79),
  ('decls -> decls decl','decls',2,'p_decls','Parser.py',80),
  ('decl -> LPAREN DECLAREFUN ID LPAREN RPAREN STRING RPAREN','decl',7,'p_decl','Parser.py',85),
  ('asserts -> assert','asserts',1,'p_asserts','Parser.py',91),
  ('asserts -> asserts assert','asserts',2,'p_asserts','Parser.py',92),
  ('assert -> LPAREN ASSERT expr RPAREN','assert',4,'p_assert','Parser.py',97),
  ('expr -> pred','expr',1,'p_expr','Parser.py',102),
  ('expr -> LPAREN AND exprs RPAREN','expr',4,'p_expr','Parser.py',103),
  ('expr -> LPAREN OR exprs RPAREN','expr',4,'p_expr','Parser.py',104),
  ('expr -> LPAREN NOT expr RPAREN','expr',4,'p_expr','Parser.py',105),
  ('exprs -> expr','exprs',1,'p_exprs','Parser.py',110),
  ('exprs -> exprs expr','exprs',2,'p_exprs','Parser.py',111),
  ('pred -> LPAREN EQUALS str str RPAREN','pred',5,'p_pred','Parser.py',116),
  ('pred -> LPAREN CONTAINS str const RPAREN','pred',5,'p_pred','Parser.py',117),
  ('pred -> LPAREN CONTAINS str error RPAREN','pred',5,'p_pred_error','Parser.py',124),
  ('str -> ID','str',1,'p_id','Parser.py',129),
  ('str -> const','str',1,'p_str','Parser.py',136),
  ('str -> LPAREN CONCAT strs RPAREN','str',4,'p_str','Parser.py',137),
  ('const -> CONST','const',1,'p_const','Parser.py',142),
  ('str -> LPAREN REPLACEALL str const const RPAREN','str',6,'p_replaceall','Parser.py',147),
  ('str -> LPAREN REPLACEALL str error const RPAREN','str',6,'p_replaceall_error','Parser.py',156),
  ('str -> LPAREN REPLACEALL str const error RPAREN','str',6,'p_replaceall_error','Parser.py',157),
  ('str -> LPAREN REPLACEALL str error error RPAREN','str',6,'p_replaceall_error','Parser.py',158),
  ('strs -> str','strs',1,'p_strs','Parser.py',163),
  ('strs -> strs str','strs',2,'p_strs','Parser.py',164),
  ('build -> LPAREN CHECKSAT RPAREN LPAREN GETMODEL RPAREN','build',6,'p_build','Parser.py',169),
]
