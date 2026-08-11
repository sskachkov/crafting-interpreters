# crafting-interpreters

Working through [*Crafting Interpreters*](https://craftinginterpreters.com) by Robert Nystrom — implementing the Lox language multiple times, in multiple languages, as I go through the book.

The book itself only asks for two implementations: a Java tree-walking interpreter (**jlox**, Part II) and a C bytecode VM (**clox**, Part III). But for Part II, I went with Python instead of Java, so overall status is:

| Directory | Language | What it actually is | Status |
|---|---|---|---|
| [`plox/`](plox) | Python | Tree-walking interpreter — fills the book's "jlox" role, just in Python | Complete (scanner → parser → resolver → interpreter, incl. classes, inheritance, closures) |
| [`clox/`](clox) | C | The book's actual Part III, following its own naming | In progress — primary/most current implementation |
| [`jlox/`](jlox) | Java | **Not** the book's tree-walker — a Java port of the bytecode VM (mirrors `clox`'s `Chunk`/`OpCode`/`Compiler`/`VM`), done for extra practice | In progress — behind `clox` |

- **plox** — feature-complete tree-walk interpreter: variables, control flow, functions/closures, classes with inheritance (`super`).
- **clox** — global & local variables, block scoping, `if`/`else`, `and`/`or` short-circuiting, jumps. Not yet implemented: `while`/`for` loops, function calls, closures, garbage collection, classes.
- **jlox** — global variables and expressions only; hasn't caught up to `clox`'s local-variable/scoping work yet.

## Running things

**clox**
```sh
make -C clox bin
./clox/clox path/to/script.lox
```

**jlox**
```sh
javac -d jlox/target/classes $(find jlox/src/main/java -name '*.java')
java -cp jlox/target/classes com.ss.jlox.Main path/to/script.lox
```
(`mvn package` also works if your local Maven cache has the required plugins.)

**plox**
```sh
python3 plox/plox.py path/to/script.lox
```

All three drop into a REPL if you run them with no script argument.

## Testing

- `clox/` has a small Unity-based C unit test suite (`make -C clox test`, builds/runs `testClox`) — currently covers bytecode line-number tracking.
- `plox/` has a pytest suite (`pytest plox/tests`) covering the scanner, parser, and interpreter.
- `scripts/test-{clox,jlox,plox}.zsh` (or `scripts/test-all.zsh`) build each implementation and smoke-test it against every `.lox` file it owns — no golden-output comparison yet, just "did it run without crashing." Pass `-v` for full interpreter output.
