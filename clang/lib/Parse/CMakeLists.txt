set(LLVM_LINK_COMPONENTS
  FrontendOpenMP
  FrontendFT
  MC
  MCParser
  Support
  TargetParser
  )

add_clang_library(clangParse
  ParseAST.cpp
  ParseCXXInlineMethods.cpp
  ParseDecl.cpp
  ParseDeclCXX.cpp
  ParseExpr.cpp
  ParseExprCXX.cpp
  ParseFT.cpp
  ParseHLSL.cpp
  ParseInit.cpp
  ParseObjc.cpp
  ParseOpenMP.cpp
  ParsePragma.cpp
  ParseStmt.cpp
  ParseStmtAsm.cpp
  ParseTemplate.cpp
  ParseTentative.cpp
  Parser.cpp

  LINK_LIBS
  clangAST
  clangBasic
  clangLex
  clangSema

  DEPENDS
  omp_gen
  ClangDriverOptions
  )
