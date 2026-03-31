public class Program5{
  public static void main(String[] args){
    ACCESSTYPE a = ACCESSTYPE.READ;
    ACCESSTYPE b = ACCESSTYPE.READ_WRITE;
    ACCESSTYPE c = ACCESSTYPE.FULL_ACCESS;

    a.read();//Allowed
    a.write();//denied
    b.write();//allowed
    b.read();//allowed
    c.read();//allowed
    a.execute();//denied
    b.execute();//denied
    c.execute();//allowed
  }

  public enum ACCESSTYPE{
    READ{
      public void read(){
        print("Read is allowed.");
      }
    },
    WRITE{
      public void write(){
        print("Writing allowed.");
      }
    },
    EXECUTE{
      public void execute(){
        print("Executing is allowed.");
      }
    },
    READ_WRITE{
      public void write(){
        print("Writing is allowed.");
      }
      public void read(){
        print("Reading is allowed.");
      }
    },
    FULL_ACCESS{
      public void read(){
        print("Reading is allowed.");
      }
      public void write(){
        print("Writing is allowed.");
      }
      public void execute(){
        print("Executing is allowed.");
      }
    };
    public void read(){
      print("ERRO: Read not allowed!");
    }
    public void write(){
      print("ERRO: writing not allowed!");
    }
    public void execute(){
      print("ERRO: Execute not allowed!");
    }
  }
  public static void print(String s){
    System.out.println(s);
  }
}

