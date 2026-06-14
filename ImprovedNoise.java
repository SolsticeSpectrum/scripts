// convert -delay 1 -dispose Background -loop 0 sequence/frame*.png output.gif

import java.awt.Canvas;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.Random;

import javax.imageio.ImageIO;
import javax.swing.JFrame;

public class ImprovedNoise extends JFrame {
    private static final String[] SYMBOLS = {
        "-", "#"
    };

    private int[] p = new int[512];
    private int[] permutation = new int[256];

    public ImprovedNoise() {
        p = new int[512];
        permutation = new int[256];

        Random rand = new Random();
        for (int i = 0; i < 256; i++) {
            permutation[i] = i;
        }
        for (int i = 0; i < 256; i++) {
            int j = rand.nextInt(256 - i) + i;
            int temp = permutation[i];
            permutation[i] = permutation[j];
            permutation[j] = temp;
        }

        for (int i = 0; i < 256; i++) {
            p[256 + i] = p[i] = permutation[i];
        }
    }

    public double zebraValley(double x, double y, double z) {
        double Ux = (x * 10) / 25.0;
        double Uy = (y * 10) / 25.0;
        double O = 0.0;

        for (double i = 0.0, v; i < 70.0; i++) {
            v = 9.0 - i / 6.0 + 2.0 * Math.cos(Ux + Math.sin(i / 6.0 + z)) - Uy;
            O = mix(O, i % 2, smoothstep(0.0, 15.0 / x / 100, v * 200));
        }

        return O;
    }

    private double mix(double x, double y, double a) {
        return x * (1.0 - a) + y * a;
    }

    public double zebraStripes(double x, double y, double z) {
        double g = 1.0;
        double t = z * 0.104;
        double centerX = Math.sin(y * g + t + z);
        double centerY = Math.cos(x * g + t);
        double d = Math.sqrt(Math.pow(x - centerX, 2) + Math.pow(y - centerY, 2));
        double k = -Math.sin(d * 1.283 * 10.0 - t);
        double e = smoothstep(0.0, Math.abs(k) * 1.5, k);

        return Math.sqrt(Math.max(e, 0.0));
    }

    private double smoothstep(double edge0, double edge1, double x) {
        double t = Math.max(0.0, Math.min(1.0, (x - edge0) / (edge1 - edge0)));
        return t * t * (3.0 - 2.0 * t);
    }

    public double terrainNoise(double x, double y, double z) {
        double total = -0.5;
        double frequency = 2.0;
        double amplitude = 1.0;

        for (int i = 0; i < 4; i++) {
            total += noise(x * frequency, y * frequency, z * frequency) * amplitude;
            frequency *= 2.0;
            amplitude *= 0.5;
        }

        return total;
    }

    public double noise(double x, double y, double z) {
        int X = (int) Math.floor(x) & 255,
                Y = (int) Math.floor(y) & 255,
                Z = (int) Math.floor(z) & 255;

        x -= Math.floor(x);
        y -= Math.floor(y);
        z -= Math.floor(z);

        double u = fade(x),
                v = fade(y),
                w = fade(z);

        int A = p[X] + Y,
                AA = p[A] + Z,
                AB = p[A + 1] + Z,
                B = p[X + 1] + Y,
                BA = p[B] + Z,
                BB = p[B + 1] + Z;

        return scale(lerp(w, lerp(v, lerp(u, grad(p[AA], x, y, z),
                grad(p[BA], x - 1, y, z)),
                lerp(u, grad(p[AB], x, y - 1, z),
                        grad(p[BB], x - 1, y - 1, z))),
                lerp(v, lerp(u, grad(p[AA + 1], x, y, z - 1),
                        grad(p[BA + 1], x - 1, y, z - 1)),
                        lerp(u, grad(p[AB + 1], x, y - 1, z - 1),
                                grad(p[BB + 1], x - 1, y - 1, z - 1)))));
    }

    private double fade(double t) {
        return t * t * t * (t * (t * 6 - 15) + 10);
    }

    private double lerp(double t, double a, double b) {
        return a + t * (b - a);
    }

    private double grad(int hash, double x, double y, double z) {
        int h = hash & 15;
        double u = h < 8 ? x : y,
                v = h < 4 ? y : h == 12 || h == 14 ? x : z;
        return ((h & 1) == 0 ? u : -u) + ((h & 2) == 0 ? v : -v);
    }

    private double scale(double n) {
        return (1 + n) / 2;
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("Usage: java ImprovedNoise --graphic|--terminal");
            System.exit(1);
        }

        String mode = args[0];

        if (mode.equals("--graphic")) {
            ImprovedNoise noise = new ImprovedNoise();

            JFrame frame = new JFrame("Perlin Noise");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setSize(800, 600);

            Canvas canvas = new Canvas();
            canvas.setPreferredSize(new Dimension(800, 600));
            frame.add(canvas);
            frame.pack();
            frame.setVisible(true);

            Graphics g = canvas.getGraphics();
            double t = 0;
            int frameNumber = 1;

            File sequenceDir = new File("sequence");
            if (!sequenceDir.exists()) {
                sequenceDir.mkdir();
            }

            for (File list : sequenceDir.listFiles()) {
                if (list.getName().endsWith(".png")) {
                    list.delete();
                }
            }

            while (true) {
                BufferedImage image = new BufferedImage(canvas.getWidth(), canvas.getHeight(), BufferedImage.TYPE_INT_ARGB/**RGB**/);
                Graphics2D g2d = image.createGraphics();

                for (int x = 0; x < canvas.getWidth(); x++) {
                    for (int y = 0; y < canvas.getHeight(); y++) {
                        double n = noise.noise(x / 100.0, y / 100.0, t);
                        g.setColor(n < 0.5 ? Color.BLACK : new Color(255, 255, 255));
                        g.fillRect(x, y, 1, 1);
                        g2d.setColor(n < 0.5 ? new Color(0, 0, 0, 0)/**Color.BLACK**/ : new Color(255, 255, 255, 255));
                        g2d.fillRect(x, y, 1, 1);
                    }
                }

                String fileName = String.format("frame%05d.png", frameNumber);
                File file = new File("sequence/" + fileName);

                try {
                    ImageIO.write(image, "png", file);
                } catch (IOException e) {
                    e.printStackTrace();
                }

                t += 0.1;
                frameNumber++;

                try {
                    Thread.sleep(1);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        } else if (mode.equals("--terminal")) {
            ImprovedNoise noise = new ImprovedNoise();
            StringBuilder sb = new StringBuilder();
            double t = 0;

            while (true) {
                for (int y = 0; y < 10; y++) {
                    for (int x = 0; x < 20; x++) {
                        double n = noise.noise(x / 5.0, y / 5.0, t);
                        sb.append(SYMBOLS[(int) (n * 2)]);
                    }
                    sb.append("\n");
                }
                System.out.println(sb.toString());

                t += 0.1;

                try {
                    Thread.sleep(50);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                System.out.print("\033[H\033[2J");
                sb.setLength(0);
            }
        } else {
            System.err.println("Usage: java ImprovedNoise --graphic|--terminal");
            System.exit(1);
        }
    }
}
