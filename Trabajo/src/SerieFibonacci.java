import java.util.Scanner;

public class SerieFibonacci {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        int n;

        System.out.print("Ingrese la cantidad de terminos a sumar: ");
        n = sc.nextInt();

        double suma = 0;

        // Variables para generar Fibonacci sin arreglos
        int f1 = 0;   // F0
        int f2 = 1;   // F1
        int fn;       // Fibonacci siguiente

        // Control de signos según el patrón observado
        // +, -, -, +, +, +, -, -, +
        int signoPosicion = 1;
        int secuenciaSignos = 1; // contador cíclico 1–9

        for (int i = 1; i <= n; i++) {

            // Generar siguiente Fibonacci
            fn = f1 + f2;
            f1 = f2;
            f2 = fn;

            // Numerador = F(i)
            int numerador = f1;

            // Denominador = F(i+1)
            int denominador = f2;

            // Termino base
            double termino = Math.sqrt((double)numerador / denominador);

            // Determinar signo según patrón
            if (secuenciaSignos == 1) signoPosicion = +1;
            else if (secuenciaSignos == 2) signoPosicion = -1;
            else if (secuenciaSignos == 3) signoPosicion = -1;
            else if (secuenciaSignos == 4) signoPosicion = +1;
            else if (secuenciaSignos == 5) signoPosicion = +1;
            else if (secuenciaSignos == 6) signoPosicion = +1;
            else if (secuenciaSignos == 7) signoPosicion = -1;
            else if (secuenciaSignos == 8) signoPosicion = -1;
            else if (secuenciaSignos == 9) signoPosicion = +1;

            // Aplicar signo
            double terminoFinal = termino * signoPosicion;

            // Mostrar cada término generado
            System.out.println("Termino " + i + ": " +
                    (signoPosicion == -1 ? "- " : "+ ") +
                    "sqrt(" + numerador + "/" + denominador + ") = " + terminoFinal);

            // Acumular suma
            suma += terminoFinal;

            // Reiniciar ciclo de signos
            secuenciaSignos++;
            if (secuenciaSignos > 9) secuenciaSignos = 1;
        }

        System.out.println("\nLa suma total de los " + n + " primeros terminos es: " + suma);
    }
}
