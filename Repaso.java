import java.util.Scanner;

public class Repaso {

    public static void main(String[] args) {
     Scanner scanner = new Scanner(System.in);

        System.out.println("INgrese un numero para procesar");
        float numero_uno = scanner.nextFloat();
        System.out.println("Ingrese otro numero");
        float numero_dos = scanner.nextFloat();


        float suma = numero_dos + numero_uno;



        float resta = numero_dos - numero_uno;



        float multiplicacion = numero_dos * numero_uno;



        float division = numero_dos / numero_uno;

        System.out.println("Suma : " + suma);
        System.out.println("Resta : " + resta);
        System.out.println("Multiplicacion : " + multiplicacion);
        System.out.println("Division : " + division);

        if (numero_dos !=0){
            System.out.println("division = " + division);

        }else {
            System.out.println("ERROR EL SEGUNDO NUMERO NO PUEDE SER 0");
        }
        scanner.close();

    }}
