/*********************************************
 * OPL 20.1.0.0 Model
 * Author: baret
 * Creation Date: 8 mars 2022 at 15:10:57
 *********************************************/
/*********************************************
 * OPL 20.1.0.0 Model
 * Author: baret
 * Creation Date: 8 mars 2022 at 11:26:27
 *********************************************/
int R=10000;

 int NbC=...;
 int NbF=...;
 int NbL=...;
 float B=...;
 float b=0.3*B;
 
 range Clients=1..NbC;
 range Facilities=1..NbF;
 range Levels=1..NbL;
 
 float h[Clients]=...;// demand
 float d[Clients, Facilities]=...;
 float c[Facilities,Levels]=...;
 float p[Clients]=...;
 float q[Facilities, Levels]=...;
 {int} K[Clients]=...;
 
 
 dvar float u[Clients];
 dvar float y[Clients,Facilities, Levels];
 dvar boolean z[Facilities,Levels];
 dvar float T;
 
 /*minimize R*(sum(i in Clients) h[i]*(((sum(k in 1..(card(K[i])-1)) d[i, item(K[i],k)]*(sum(l in Levels) (1-q[item(K[i],k),l])*y[i,item(K[i],k),l]))+p[i]*u[i])));
 */
 minimize R*(sum(i in Clients) h[i]*((sum(k in 1..card(K[i])-1) d[i,item(K[i],k)] * sum(l in Levels) (1-q[item(K[i],k),l])*y[i,item(K[i],k),l])+p[i]*u[i]));
 subject to {
   forall(i in Clients) R*sum(l in Levels) y[i,item(K[i],1),l]==R*1;
   forall(i in Clients, k in 1..card(K[i])-2) R*(sum(l in Levels) q[item(K[i],k),l]*y[i,item(K[i],k),l])== R*sum(l in Levels) y[i,item(K[i],k+1),l];
   forall (i in Clients) R*sum(l in Levels) (q[last(K[i]),l]*y[i,last(K[i]),l])==R*u[i];
   forall(i in Clients, k in 1..(card(K[i])-1),l in Levels) R*y[i,item(K[i],k),l] <= R*z[item(K[i],k),l];
   sum(k in Facilities, l in Levels ) R*c[k,l]*z[k,l]<=R*b;
   forall( k in Facilities) sum(l in Levels) R*z[k,l]==R*1;
   forall(i in Clients, k in Facilities, l in Levels) R*y[i,k,l]<=R*1;
   forall(i in Clients, k in Facilities, l in Levels) R*y[i,k,l]>=R*0;
   forall(i in Clients) R*u[i]<=R*1;
   forall(i in Clients) R*u[i]>=R*0;
   
  /* T==sum(i in Clients)h[i]*prod(k in 1..card(K[i])-1)sum(l in Levels)q[item(K[i],k),l]*z[item(K[i],k),l]*p[i];*/
 }