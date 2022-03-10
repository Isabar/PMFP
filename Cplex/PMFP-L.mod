/*********************************************
 * OPL 20.1.0.0 Model
 * Author: baret
 * Creation Date: 8 mars 2022 at 11:26:27
 *********************************************/

 int NbC=...;
 int NbF=...;
 int NbL=...;
 float B=...;
 float b=0.45*B;
 
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
 
 //minimize sum(i in Clients) h[i]*(((sum(k in 1..(card(K[i])-1)) d[i, item(K[i],k)]*(sum(l in Levels) (1-q[item(K[i],k),l])*y[i,item(K[i],k),l]))+p[i]*u[i]));
 minimize sum(i in Clients) h[i]*p[i]*u[i];
 subject to {
   forall(i in Clients) sum(l in Levels) y[i,item(K[i],1),l]==1;
   forall(i in Clients, k in 1..card(K[i])-2) (sum(l in Levels) q[item(K[i],k),l]*y[i,item(K[i],k),l])== sum(l in Levels) y[i,item(K[i],k+1),l];
   forall (i in Clients) sum(l in Levels) (q[last(K[i]),l]*y[i,last(K[i]),l])==u[i];
   forall(i in Clients, k in 1..(card(K[i])-1),l in Levels) y[i,item(K[i],k),l] <= z[item(K[i],k),l];
   sum(k in Facilities, l in Levels ) c[k,l]*z[k,l]<=b;
   forall( k in Facilities) sum(l in Levels) z[k,l]==1;
   forall(i in Clients, k in Facilities, l in Levels) y[i,k,l]<=1;
   forall(i in Clients, k in Facilities, l in Levels) y[i,k,l]>=0;
   forall(i in Clients) u[i]<=1;
   forall(i in Clients) u[i]>=0;
 }