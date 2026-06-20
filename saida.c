#include <stdio.h>

int ligar(char* name) { printf("%s ligado!\n", name); return 1; }
int desligar(char* name) { printf("%s desligado!\n", name); return 0; }
int verificar(char* name) { printf("%s estado verificado.\n", name); return 1; }
void alerta_msg(char* name, char* msg) { printf("%s recebeu o alerta: \n%s\n", name, msg); }
void alerta_var(char* name, char* msg, int var) { printf("%s recebeu o alerta: \n%s %d\n", name, msg, var); }
int agendar(char* name, char* hora) { printf("Alarme agendado no %s para as %s\n", name, hora); return 1; }
int fechar(char* name) { printf("%s fechado!\n", name); return 1; }

int main() {
    int fumaca = 0;
    int temperatura = 0;
    int cinema = 0;
    int dormir = 0;

    fumaca = 0;
    temperatura = 28;
    cinema = 1;
    dormir = 0;
    verificar("Luz_Sala");
    if (fumaca == 1) {
        alerta_var("Celular", "Perigo de incendio", fumaca);
        alerta_msg("TV", "Evacuar imediatamente");
        alerta_msg("Celular", "Evacuar imediatamente");
        alerta_msg("Luz_Sala", "Evacuar imediatamente");
    }
    if (temperatura > 25) {
        ligar("Ar_Condicionado");
    }
    if (cinema == 1 && fumaca == 0) {
        fechar("Cortina");
        ligar("TV");
        desligar("Luz_Sala");
        alerta_msg("Alexa", "Alexa, ligar aura!");
    } else {
        desligar("TV");
    }
    if (dormir == 1) {
        agendar("Celular", "07:00");
        fechar("Cortina");
        desligar("Luz_Sala");
    }
    return 0;
}
