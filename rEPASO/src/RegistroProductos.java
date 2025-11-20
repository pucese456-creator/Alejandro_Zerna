import java.util.Scanner;

public class RegistroProductos {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int limiteProductos = 0;


        while (limiteProductos <= 0) {
            System.out.print("Ingrese el limite maximo de productos para hoy: ");
            limiteProductos = sc.nextInt();

            if (limiteProductos <= 0) {
                System.out.println("El limite debe ser un numero positivo. Intente de nuevo.");
            }
        }


        int cantidadProductos = 0;
        double totalIVA = 0.0;
        double totalIMC = 0.0;
        double totalVentas = 0.0;


        sc.nextLine();


        for (int i = 1; i <= limiteProductos; i++) {
            System.out.println("\n=== Producto #" + i + " ===");


            System.out.print("Nombre del producto: ");
            String nombre = sc.nextLine();


            double precioBase = -1;
            while (precioBase <= 0) {
                System.out.print("Precio base del producto: ");
                precioBase = sc.nextDouble();

                if (precioBase <= 0) {
                    System.out.println("El precio debe ser un numero positivo. Intente de nuevo.");
                }
            }


            int aplicaIVA = -1;
            while (aplicaIVA != 0 && aplicaIVA != 1) {
                System.out.print("El producto tiene IVA? (1 = si, 0 = no): ");
                aplicaIVA = sc.nextInt();

                if (aplicaIVA != 0 && aplicaIVA != 1) {
                    System.out.println("Opcion invalida. Solo se acepta 0 o 1.");
                }
            }


            double iva = 0.0;
            if (aplicaIVA == 1) {
                iva = 0.12 * precioBase;
            }

            double imc = 0.015 * precioBase;

            double precioFinal = precioBase + iva + imc;


            System.out.println("\nResumen del producto:");
            System.out.println("Nombre: " + nombre);
            System.out.println("Precio base: " + precioBase);
            System.out.println("IVA: " + iva);
            System.out.println("IMC: " + imc);
            System.out.println("Precio final: " + precioFinal);


            cantidadProductos++;
            totalIVA += iva;
            totalIMC += imc;
            totalVentas += precioFinal;


            sc.nextLine();
        }


        System.out.println("\n=== Resumen del dia ===");
        System.out.println("Cantidad total de productos ingresados: " + cantidadProductos);
        System.out.println("Total recaudado en IVA: " + totalIVA);
        System.out.println("Total recaudado en IMC: " + totalIMC);
        System.out.println("Monto total de ventas (precios finales): " + totalVentas);

        sc.close();
    }
}