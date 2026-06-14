// convert -delay 1 -dispose Background -loop 0 trimmed_sequence/frame*.png output.gif

import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.concurrent.TimeUnit;
import javax.imageio.ImageIO;
import javax.swing.*;

public class TextAnimation extends JFrame {
    private static final String[] ANIMATIONS = {
        "inflate", "spin", "squeeze", "slidehoriz", "slidevert", "circle"
    };

    private static final String[] TEXTS = {
        "TOHLE BYLO",
        "VYTVOŘENO",
        "V JAVĚ",
        "JEN ABYCH",
        "TI ŘEKL",
        "ŽE SMRDÍŠ"
    };

    private static String currentAnimation;
    private static Canvas canvas;

    private static void renderText(Graphics2D g2d, String text, int frameCount) {
        int fontSize = 130;
        Font font = new Font("Impact", Font.PLAIN, fontSize);
        g2d.setFont(font);
        g2d.setColor(new Color(200, 200, 56));

        if (currentAnimation.equals("inflate")) {
            float scaleFactor = (float) Math.abs(Math.sin(frameCount * Math.PI / 50));
            fontSize = (int) (80 + 80 * scaleFactor);
            font = font.deriveFont(Font.PLAIN, fontSize);
            g2d.setFont(font);
        } else if (currentAnimation.equals("spin")) {
            double angle = Math.toRadians(frameCount * 3);
            //g2d.setColor(new Color(56, 200, 92));
            g2d.rotate(angle, canvas.getWidth() / 2, canvas.getHeight() / 2);
        } else if (currentAnimation.equals("squeeze")) {
            double scaleY = Math.abs(Math.sin(frameCount * Math.PI / 50));
            //g2d.setColor(new Color(56, 150, 200));
            g2d.scale(1.0, scaleY * 1.5);
        } else if (currentAnimation.equals("slidehoriz")) {
            int xOffset = frameCount * 12;
            //g2d.setColor(new Color(164, 56, 200));
            g2d.translate(-600 + xOffset, 0);
        } else if (currentAnimation.equals("slidevert")) {
            int yOffset = frameCount * 9;
            //g2d.setColor(new Color(200, 56, 58));
            g2d.translate(0, -400 + yOffset);
        } else if (currentAnimation.equals("circle")) {
            double progress = (double) frameCount / 50;
            double angle = progress * 2 * Math.PI;
            int xCircle = (int) (90 * Math.sin(angle));
            int yCircle = (int) (220 * Math.cos(angle));
            g2d.translate(xCircle, yCircle - 25);
        }

        int textX = (canvas.getWidth() - g2d.getFontMetrics().stringWidth(text)) / 2;
        int textY = canvas.getHeight() / 2 + g2d.getFontMetrics().getHeight() / 2;
        g2d.drawString(text, textX, textY);
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Text Animation");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 600);

        canvas = new Canvas();
        canvas.setPreferredSize(new Dimension(800, 600));
        frame.add(canvas);
        frame.pack();
        frame.setVisible(true);

        Graphics g = canvas.getGraphics();

        String currentText;
        int animationFrameCount;
        int frameNumber = 1;
        int currentTextIndex = 0;

        for (String animation : ANIMATIONS) {
            currentAnimation = animation;
            animationFrameCount = 0;

            currentText = TEXTS[currentTextIndex];
            currentTextIndex = (currentTextIndex + 1) % TEXTS.length;

            for (int i = 0; i < 120; i++) {
                BufferedImage image = new BufferedImage(canvas.getWidth(), canvas.getHeight(), BufferedImage.TYPE_INT_ARGB/**RGB**/);
                Graphics2D g2d = image.createGraphics();
                g.setColor(Color.WHITE);
                g.fillRect(0, 0, canvas.getWidth(), canvas.getHeight());
                g2d.setColor(new Color(0, 0, 0, 0)/**Color.BLACK**/);
                g2d.fillRect(0, 0, canvas.getWidth(), canvas.getHeight());

                renderText(g2d, currentText, animationFrameCount);
                animationFrameCount++;

                Graphics canvasGraphics = canvas.getGraphics();
                canvasGraphics.drawImage(image, 0, 0, canvas);
                canvasGraphics.dispose();

                File sequenceDir = new File("sequence");
                if (!sequenceDir.exists()) {
                    sequenceDir.mkdir();
                }

                String fileName = String.format("frame%05d.png", frameNumber);
                File file = new File("sequence/" + fileName);
                try {
                    ImageIO.write(image, "png", file);
                } catch (IOException e) {
                    e.printStackTrace();
                }

                frameNumber++;

                try {
                    TimeUnit.MILLISECONDS.sleep(17);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                if (currentTextIndex == 0 && i == 119) {
                    System.exit(0);
                }
            }

            try {
                TimeUnit.MILLISECONDS.sleep(17);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
