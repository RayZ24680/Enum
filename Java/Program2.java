public class Program2{

  public enum DIGIT{
        ZERO,
        ONE,
        TWO,
        THREE,
        FOUR,
        FIVE;
    }

  public static void print(String s){
    System.out.println(s);
  }

  public static void main(String[] args){
    DIGIT num = DIGIT.FOUR;
    switch(num){
      case ONE:
        print("1");
        break;
      case TWO:
        print("2");
        break;
      case FOUR:
        print("4");
        break;
      default:
        print("Case Not Found!");
        break;
    }
    //The switch is missing case FIVE, ZERO and THREE but java allows it.
  }
}
