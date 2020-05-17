import java.util.ArrayList;
public class helloworld1
{
    public static void main(String[] args)
    {
        String alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ";
        String result = "Hello world";
        ArrayList<Character> list = new ArrayList();
        for(int j = 0; j < result.length(); j++)
        {
            char rsubstring = result.charAt(j);
            for(int i = 0; i < alphabet.length(); i++)
            {
                char substring = alphabet.charAt(i);
                if(substring == rsubstring)
                {
                    list.add(substring);
                }
            }
        }
        String yuy = "";
        for(char elem : list)
        {
            yuy += elem;
        }
        System.out.println(yuy);
    }
}