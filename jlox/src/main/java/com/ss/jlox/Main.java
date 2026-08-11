package com.ss.jlox;

import java.io.*;

public class Main {
    public static void main(String[] args) {
        System.setProperty("debug.traceExecution", "true");
        System.setProperty("debug.printCode", "true");
        if (args.length == 0) {
            repl();
        } else {
            runFile(args[0]);
        }
        //exec(args);
    }

    private static void repl() {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        VM vm = new VM();
        for (; ; ) {
            System.out.print("> ");
            try {
                String line = reader.readLine();
                line = line.trim();
                if (line.isEmpty()) {
                    return;
                }
                VM.InterpretResult result = vm.interpret(line);
                if (result == VM.InterpretResult.COMPILE_ERROR)
                    System.err.println("compile error");
                if (result == VM.InterpretResult.RUNTIME_ERROR)
                    System.err.println("runtime error");

            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }

    private static void runFile(String filename) {
        VM vm = new VM();
        String source = readFile(filename);
        //System.out.println(source);
        VM.InterpretResult result = vm.interpret(source);
        if (result == VM.InterpretResult.COMPILE_ERROR)
            System.exit(65);
        if (result == VM.InterpretResult.RUNTIME_ERROR)
            System.exit(70);
    }


    private static String readFile(String filename) {
        File f = new File(filename);
        StringBuilder sb = new StringBuilder();
        try (FileInputStream fis = new FileInputStream(f)) {
            BufferedReader br = new BufferedReader(new InputStreamReader(fis));
            String line = br.readLine();
            while (line != null && !line.isEmpty()) {
                sb.append(line).append("\n");
                line = br.readLine();
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return sb.toString();
    }

}
