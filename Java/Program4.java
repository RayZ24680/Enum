public class Program4{


  public enum DIGIT{
    ONE,TWO,THREE,FOUR,FIVE;
    //ONE; Java doesnt allow enum instances with the same name to be declared previously.
  }
  //a list called values is automatically assigned to any initialized enum and can be accessed by .values().

  public static void print(String s){
    System.out.println(s);
  }

  public static void main(String[] args){
    //iterate of DIGIT's values using enhanced foor loop.
    for(DIGIT d : DIGIT.values()){
      print(d  + " -> " + d.ordinal());
      
    }
  }
}
