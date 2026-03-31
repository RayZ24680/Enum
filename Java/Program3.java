public class Program3{


  public enum SHAPE{
    CIRCLE(2.0){
      @Override
      public double area(double r){
        return Math.PI * r * r;
      }
      public double area(){
          return Math.PI * this.r * this.r;
      }
    },
    RECTANGLE(4.0,5.0){
      public double area(double l, double h){
        return l*h;
      }
      public double area(){
          return this.len * this.wid;
      }
    },
    TRIANGLE(4.0,2.0){
      public double area(double l, double h){
        return (0.5) * l * h;
      }
      public double area(){
          return 0.5 * this.wid * this.len;
      }
    };
    public double r;
    public double len;
    public double wid;
    SHAPE(double r){
        this.r = r;
    }
    SHAPE(double l, double w){
        this.wid = w;
        this.len = l;
    }
    public double area(double l, double h){return 0.0;}
    public double area(double r){return 0.0;}
    public double area(){return 0.0;}
    //Each enum instance can overrride the commonly desclared methods in the enum namespace.
  }

  public static void print(double d){
    System.out.println(d);
  }
  public static void main(String[] args){
    SHAPE rect = SHAPE.RECTANGLE;
    SHAPE circle = null;
    SHAPE tri = SHAPE.TRIANGLE;

    print(rect.area(3.0,4.0));//works
    print(rect.area());//works
    print(tri.area(3.0,4.0));//works
    // print(circle.area(2.0));// error cicle may not have been initialized (error);
    //using unassigned variables or null assigned variables can lead to not initialized error or NULLPOINTEREXCEPTION.
    
  }








  
}
