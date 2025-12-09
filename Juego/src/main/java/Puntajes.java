import javax.swing.JOptionPane;

public class Puntajes {
    public static void main(String[] args) {

        int cantidad = 0;

        // Pedir cantidad entre 5 y 15
        while (cantidad < 5 || cantidad > 15) {
            String textoCantidad = JOptionPane.showInputDialog(
                    "Ingrese la cantidad de puntajes (entre 5 y 15):");
            cantidad = Integer.parseInt(textoCantidad);
        }

        int[] puntajes = new int[cantidad];

        // Pedir cada puntaje entre 0 y 100
        for (int i = 0; i < cantidad; i++) {
            int p = -1;
            while (p < 0 || p > 100) {
                String textoPuntaje = JOptionPane.showInputDialog(
                        "Ingrese el puntaje #" + (i + 1) + " (0 a 100):");
                p = Integer.parseInt(textoPuntaje);
            }
            puntajes[i] = p;
        }

        // Calcular máximo, mínimo, promedio y cantidad >= 90
        int maximo = puntajes[0];
        int minimo = puntajes[0];
        int suma = 0;
        int conteoMayores90 = 0;

        for (int i = 0; i < cantidad; i++) {
            int valor = puntajes[i];

            if (valor > maximo) {
                maximo = valor;
            }
            if (valor < minimo) {
                minimo = valor;
            }

            suma = suma + valor;

            if (valor >= 90) {
                conteoMayores90 = conteoMayores90 + 1;
            }
        }

        double promedio = (double) suma / cantidad;

        JOptionPane.showMessageDialog(null,
                "RESULTADOS GENERALES\n" +
                        "Puntaje más alto: " + maximo + "\n" +
                        "Puntaje más bajo: " + minimo + "\n" +
                        "Promedio: " + promedio + "\n" +
                        "Cantidad de puntajes >= 90: " + conteoMayores90);

        // Menú
        int opcion = 0;

        while (opcion != 4) {

            String textoOpcion = JOptionPane.showInputDialog(
                    "MENÚ\n" +
                            "1. Ver todos los puntajes\n" +
                            "2. Ver puntajes aprobados (>= 60)\n" +
                            "3. Ver puntajes reprobados (< 60)\n" +
                            "4. Salir\n\n" +
                            "Elija una opción:");
            opcion = Integer.parseInt(textoOpcion);

            if (opcion == 1) {
                String mensaje = "TODOS LOS PUNTAJES:\n";
                for (int i = 0; i < cantidad; i++) {
                    mensaje = mensaje + puntajes[i] + " ";
                }
                JOptionPane.showMessageDialog(null, mensaje);
            }

            if (opcion == 2) {
                String mensaje = "PUNTAJES APROBADOS (>= 60):\n";
                for (int i = 0; i < cantidad; i++) {
                    if (puntajes[i] >= 60) {
                        mensaje = mensaje + puntajes[i] + " ";
                    }
                }
                JOptionPane.showMessageDialog(null, mensaje);
            }

            if (opcion == 3) {
                String mensaje = "PUNTAJES REPROBADOS (< 60):\n";
                for (int i = 0; i < cantidad; i++) {
                    if (puntajes[i] < 60) {
                        mensaje = mensaje + puntajes[i] + " ";
                    }
                }
                JOptionPane.showMessageDialog(null, mensaje);
            }
        }
    }
}