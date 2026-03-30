public class MAIN{

    //Enums can be defined as...
    public enum DIGIT{
        ZERO(0),
        ONE(1),
        ONe(1),//Allowed in java same values don't cause errors as long as name is different.
        //ONE(1), Not allowed in java error already defined!
        TWO(2),
        THREE(3),
        FOUR(4);

        //enums in java can have their own methods and act like classes
        private int val;
        //enums can also have multiple constructors like classes
        DIGIT(int value){
            this.val = value;
        }
    }

    //enums are assigned a list called values at assignment it contains all enums of the type
    //enums can also have a common abstract method which each object can override seperately
    public enum SHAPE{
        CIRCLE{
            @Override
            public double area(double a, double b){
                return Math.PI * a * b;//a == b (b = radius)
            }
        },
        RECTANGLE{
            @Override
            public double area(double a, double b){
                return a*b;
            }
        },
        TRIANGLE{
            @Override
            public double area(double a, double b){
                return (1/2.0) * a * b;
            }
        };
        public abstract double area(double a, double b);
    }


    public static void main(String[] args){
        //iterating over the enum.
        for(DIGIT d : DIGIT.values()){
            System.out.println(d + " -> " + d.ordinal());
        }

        //Conversion
        // int one = DIGIT.ONE; not allowed incompatible type
        // int one = (int)DIGIT.ONE;Cannot be converted to int (Stringly typed)
        //Equality test
        // System.out.print(DIGIT.ONE == 1); Bad operand types error
        DIGIT dig1 = DIGIT.ONE;
        DIGIT dig2 = DIGIT.ONE;
        DIGIT two = DIGIT.TWO;
        if(dig1 == dig2){
            print("\'==\'can be used to compare enum instances");
        }
        /*Enum in java cannot be compared using comparison operators.
        if(dig1 < two){
            print("1 < 2");
        }
        */
        //Comparison even though enum instances cannot be compared using <, >, <=, >= they implement Comparable interface which allows them to use thier ordinal value(order they were declared and initialized) to determine their value.
        if(dig1.compareTo(two) < 0){
            print("1 < 2");
        }

        //Mutability
        // DIGIT.ONE = 10; incompatible types
        //Java enums can not be changed or created during runtime they are static final variables.

        //Switch case statement
        //Java enums are compatible with switch statements.
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
                print("Case not found");
                break;
            //cases ZERO and FIVE, and ONe are missing but java allows the switch without any alerts.
        }

        //Using enum methods
        SHAPE rect = SHAPE.RECTANGLE;
        print("Area: " + rect.area(2.0,4.0));
        //Calling enum method for an unassigned/NULL enum.
        SHAPE circle;
        // double a = circle.area(2.2,2.2);//circle may not have been intialized (error)

    }

    public static void print(String s){
        System.out.println(s);
    }

}
