import java.awt.Color;


public class Zebra {
    private int N;                     // N-by-N grid of cells
    private int MAXDIST = 3;           // definition of neighbor
    private boolean[][] cells;         // cell[i][j] = true if alive, false o/w
    private Picture pic;

    // nice pattern
    // double[] weight = {2.0, 2.0, -0.4, -0.4};
    // double threshhold = 1.4;

    // zebra stripes
    double[] weight = {2.0, 2.0, -1.2, -1.2};
    double threshhold = 1.4;


    public Zebra(int N) {
        this.N = N;
        this.cells = new boolean[N][N];
        pic = new Picture(N, N);

        // initialize with random pattern
        for (int i = 0; i < N; i++)
            for (int j = 0; j < N; j++)
                cells[i][j] = Math.random() < 0.5;

    }

    public void update() {
        int dist;
        boolean color;

        // update cells
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++)  {

                // update cell (i, j) by looking at neighbors
                double sum = 0.0;
                for (int ii = i - MAXDIST; ii <= i + MAXDIST; ii++) {
                    for (int jj = j - MAXDIST; jj <= j + MAXDIST; jj++) {
                        //// dist = Math.abs(ii-i) + Math.abs(jj-j);
                        dist = Math.abs(ii-i);

                        // uses most up-to-date values, avoid out-of-bounds
                        color = cells[(ii + N) % N][(jj + N) % N];

                        // if (dist <= MAXDIST && color) sum += weight[dist];
                        if (color) sum += weight[dist];
                    }
                }
                if (sum > threshhold) cells[i][j] = true;
                else cells[i][j] = false;
            }
        }
    }

    // draw cells
    public void draw() {
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                if (cells[i][j]) pic.set(i, j, Color.BLACK);
                else            pic.set(i, j, Color.WHITE);
            }
        }
        pic.show();
    }

    // test client
    public static void main(String[] args) {
        int N = Integer.parseInt(args[0]);
        Zebra zebra = new Zebra(N);

        for (int i = 0; i < 10; i++) {
            StdOut.println(i);
            zebra.update();
            zebra.draw();
        }
    }

}
