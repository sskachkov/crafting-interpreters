package com.ss.jlox;

public class SystemPropertyUtils {
    public static boolean getValueBool(String key) {
        String property = System.getProperty(key);
        return property != null && property.equalsIgnoreCase("true");
    }
}
