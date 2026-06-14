import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class WaveAnimation extends JPanel implements ActionListener {

    private Timer timer;
    private int frameCount = 0;

    public WaveAnimation() {
        timer = new Timer(20, this);
        timer.start();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;

        int fontSize = 30;
        int param = 5;

        String text = "WAVE";
        Font font = new Font("Arial", Font.BOLD, fontSize);

        for (int i = 0; i < 26; i++) {
            int key = i;
            int x = -30 + (key * param);
            int y = 0;

            int[] xPoints = {x, x + 10, x + 60, x + 50};
            int[] yPoints = {y, y, y + 100, y + 100};

            g2d.setFont(font);
            g2d.setColor(new Color(0, 30, 100));
            g2d.translate(100, 100);
            g2d.rotate(Math.toRadians(20 * Math.sin(frameCount * Math.PI / 100)));
            g2d.scale(1.0 + 0.2 * Math.sin(frameCount * Math.PI / 100), 1.0 + 0.2 * Math.sin(frameCount * Math.PI / 100));
            g2d.setColor(new Color(50, 230, 255));
            g2d.fillPolygon(xPoints, yPoints, 4);
            g2d.scale(1.0 / (1.0 + 0.2 * Math.sin(frameCount * Math.PI / 100)), 1.0 / (1.0 + 0.2 * Math.sin(frameCount * Math.PI / 100)));
            g2d.rotate(Math.toRadians(-20 * Math.sin(frameCount * Math.PI / 100)));
            g2d.translate(-100, -100);
        }
        frameCount++;
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        repaint();
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Wave Animation");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 400);
        frame.add(new WaveAnimation());
        frame.setVisible(true);
    }
}
