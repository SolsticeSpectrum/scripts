               /* compile with gcc -o donut donut.c -lm */
 /* thanks https://github.com/CarboSauce for helping me with this code */
/* original code https://www.a1k0n.net/2021/01/13/optimizing-donut.html */

#define s 6  // changes the size of the donut                        8  / 6  / 6
#define l 40 // changes the position from the first row on the left  20 / 32 / 40
#define u 11 // changes the position from the top line               8  / 12 / 11
#define w 80 // changes the number of rows                           39 / 65 / 80
#define p 22 // changes the number of lines                          15 / 24 / 22

              i,j,k,x,y,o,N;
         main(){float  z[1760],a
      #define R(t,x,y)  f=x;x-=t*y\
   ;y+=t*f;f=(3-x*x-y*y)/2; x*=f;y*=f;
   =0,e=1,c=1,d=0,f,g,h,G,H,A,t,D;char
  b[1760];for(;;){memset(b,32,1760);g=0,
 h=1; memset(z,0,7040);for(j=0;j<90;j++){
G=0,H=1;for(i=0;i<314;i++){A=h+2, D=1/(G*
A*a+g*e+s);t=G*A         *e-g*a; x=l+30*D
*(H*A*d-t*c);y=           u+15*D*( H*A*c+
t*d);o=x+w*y;N             =8*((g*a-G*h*e)
*d-G*h*a-g*e-H*h          *c); if(p>y&&y>
 0&&x>0&&w>x&&D>z[o]) {z[o]=D; b[o]=(N>0
 ?N:0)[".,-~:;=!*#$@"]; }R(.02,H,G); }R(
  .07,h,g); }for(k=0;p*w>k; k++)putchar
   (k%w?b[k]:10); R(.04,e,a); R(.02,d,
     c);usleep(30000);printf( '\n'+(
       "donut.c!\x1b[23A"));printf
           ("\e[1;1H\e[2J");}}
              /* donut.c */
