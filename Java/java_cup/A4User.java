import java.io.*;
// /\*\*(.|\r|\n|\t)*?\*\*/
// /\*\*([^*]*\*+)*[^/]*\*/
class A4User {
    public static void main(String[] args) throws Exception {
        File inputFile = new File("A4.tiny");
        A4Parser parser = new A4Parser(new A4Scanner(new FileInputStream(inputFile)));
        String result = (String) parser.debug_parse().value;
        FileWriter fw = new FileWriter("src/A4.java");
        fw.write(result);
        fw.close();
    }
}