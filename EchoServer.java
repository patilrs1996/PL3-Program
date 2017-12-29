//Program for Multithreaded echo server

//SERVER PROGRAM

import java.net.*; 
import java.io.*; 

public class EchoServer 
{         
    ServerSocket ss; 
       DataInputStream dis;
    DataOutputStream dos;
     
    public EchoServer()  
    { 
        try 
        { 
           
            ss = new ServerSocket(6666); 
        } 
        catch(IOException ioe) 
        { 
            System.out.println("Could not create server socket at 6666"); 
            System.exit(-1); 
        } 
         
        System.out.println("Listening for clients on 6666"); 
         
        
        int id = 0; 
        while(true) 
        {                         
            try 
            { 
               
                Socket clientSocket = ss.accept(); 
             
                 
                ClientThread ct = new ClientThread(clientSocket, id++); 
                ct.start(); 
		dis= new DataInputStream(clientSocket.getInputStream());
            dos= new DataOutputStream(clientSocket.getOutputStream());
            } 
            catch(IOException ioe) 
            { 
                System.out.println("Exception occured :"); 
                ioe.printStackTrace(); 
            } 
        } 
    } 
     
    public static void main (String[] args) 
    { 
        new EchoServer();     
    } 
     
     
    class ClientThread extends Thread 
    { 
        Socket ss;         
        int m_clientID = -1; 
        boolean m_bRunThread = true; 
         
        ClientThread(Socket s, int clientID) 
        { 
           ss = s; 
            m_clientID = clientID; 
        } 
        
        public void run() 
        {             
            
           // BufferedReader in = null;  
           // PrintWriter out = null; 
             
          
            System.out.println("Accepted Client : ID - " + m_clientID + " : Address - " +  
                             ss.getInetAddress().getHostName()); 
                 
            try 
            {                                 
               // in = new BufferedReader(new InputStreamReader(ss.getInputStream())); 
               // out = new PrintWriter(new OutputStreamWriter(ss.getOutputStream())); 
                 

                while(m_bRunThread) 
                {                     
                 
		String str, s1;
         do
         {
             str=dis.readUTF();
             System.out.println("Client Message:"+str);
             BufferedReader br=new BufferedReader(new   InputStreamReader(System.in));
             s1=br.readLine();
             dos.writeUTF(s1);
             dos.flush();
         }
         while(!s1.equals("bye"));
                } 
            } 
            catch(Exception e) 
            { 
                e.printStackTrace(); 
            } 
            finally 
            { 
               
                try 
                {                     
                    //in.close(); 
                   // out.close(); 
                    ss.close(); 
                    System.out.println("Stopped"); 
                } 
                catch(IOException ioe) 
                { 
                    ioe.printStackTrace(); 
                } 
            } 
        }
/*OUTPUT SERVER
student@localhost ~]$ javac EchoServer.java
[student@localhost ~]$ java EchoServer
Listening for clients on 6666
Accepted Client : ID - 0 : Address - localhost.localdomain
Client Message:hi
hello
Client Message:here is preeti
here is nilam
Client Message:stop
bye
java.io.EOFException
	at java.io.DataInputStream.readUnsignedShort(DataInputStream.java:340)
	at java.io.DataInputStream.readUTF(DataInputStream.java:589)
	at java.io.DataInputStream.readUTF(DataInputStream.java:564)
	at EchoServer$ClientThread.run(EchoServer.java:89)
Stopped
*/ 
    } 
} 

//PROGRAM FOR ECHO CLIENT

import java.net.*; 
import java.io.*; 


public class EchoClient 
{ 

	
    public static void main(String[] args) 
    { 
	 

	Socket s = null; 
	    String host = "localhost";
            int port = 6666;
          InetAddress address;
		//String address = "11.11.3.158";  // Indicating the place to put Server's IP

         	DataInputStream din;
    DataOutputStream dout;
        
        try 
        { 
	   address = InetAddress.getByName(host);

            s = new Socket(address, port);
		
           
        }         
        catch(UnknownHostException e) 
        { 
           
            System.out.println(e); 
           
        } 
        catch(IOException ioe) 
        { 
           
            System.out.println("Cant connect to server at 6666."); 
           
        } 
         
        if(s == null) 
            System.exit(-1); 
 
         
        BufferedReader in = null; 
        PrintWriter out = null; 
         
        try 
        { 
            
           // in = new BufferedReader(new InputStreamReader(s.getInputStream())); 
           // out = new PrintWriter(new OutputStreamWriter(s.getOutputStream())); 
		BufferedReader br= new BufferedReader(new InputStreamReader(System.in));
		din= new DataInputStream(s.getInputStream());
             dout= new DataOutputStream(s.getOutputStream());
           String s1;
           do
           {
               s1=br.readLine();
               dout.writeUTF(s1);
               dout.flush();
               System.out.println("Server Message:"+din.readUTF());
           }
           while(!s1.equals("stop"));
             
           
        } 
        catch(IOException ioe) 
        { 
            System.out.println("Exception during communication. "); 
        } 
        finally 
        { 
            try 
            { 
               
                out.close(); 
                in.close(); 
              
                s.close(); 
            } 
            catch(Exception e) 
            { 
                e.printStackTrace(); 
            }                 
        }         
    } 
} 
/* OUTPUT CLIENT :-
[student@localhost ~]$ javac EchoClient.java
[student@localhost ~]$ java EchoClient
hi
Server Message:hello
here is preeti
Server Message:here is nilam
stop
Server Message:bye
java.lang.NullPointerException
	at EchoClient.main(EchoClient.java:79)
[student@localhost ~]$ 
*/
