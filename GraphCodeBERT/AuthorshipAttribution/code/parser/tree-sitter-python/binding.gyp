{
  "targets": [
    {
      "target_name": "tree_sitter_python_binding",
      "include_dirs": [
        "<!(node -e \"require('nan')\")",
        "src"
      ],
      "sources": [
        "src/parser.c",
        "bindings/node/binding.cc",
        "src/scanner.c"
      ],
      "cflags_c": [
        "-std=c99",
      ]
    }
  ]
}
