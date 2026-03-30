public class Program1{

  //enums can be defined as...
  public enum DIGIT{
    ZERO,ONE,TWO,THREE,FOUR;
  }

  public static void print(String s){
    System.out.println(s);
  }


  public static void main(String args[]){
    // int i = DIGIT.ONE; Error incompatible types.
    // int i = (int)DIGIT.ONE; Error enum can not be converted to int (no explicit or implicit conversion).
    DIGIT a = DIGIT.ONE;
    System.out.println(a + " -> " + a.ordinal());
    
  }
}
