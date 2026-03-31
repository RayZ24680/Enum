public class Program3{


  public enum SHAPE{
    CIRCLE{
      @Override
      public double area(double r){
        return Math.PI * r * r;
      }
    },
    RECTANGLE{
      public double area(double l, double h){
        return l*h;
      }
    },
    TRIANGLE{
      public double area(double l, double h){
        return (0.5) * l * h;
      }
    };
    public abstract double area(double l, double h);
    public abstract double area(double r);
    //Each enum instance can overrride the commonly desclared methods in the enum namespace.
  }

  public static void print(double d){
    System.out.println(d);
  }
  public static void main(String[] args){
    SHAPE rect = SHAPE.RECTANGLE;
    SHAPE circle = null;
    SHAPE tri = SHAPE.TRIANGLE;

    print(rect.area(3.0,4.0));
    print(tri.area(3.0,4.0));
    // print(circle.area(2.0)); causes NULLPOINTEREXCEPTION.
    //using unassigned variables or null assigned variables can lead to not initialized error or NULLPOINTEREXCEPTION.
    
  }








  
}
