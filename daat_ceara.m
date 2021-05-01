% DAAT/PLEDS para a boia do Ceara do PNBOIA

% Henrique e Parente

clear, clc, close all

% carrega arquivos

%table of sines and cosines for the mem method - tecnica de maxima entropia
%cria variaveis a23 e a24, com 360 colunas, que faz um circulo de 1 a -1
load lyg2.mat;


path_lista_mes = '/home/hp/Documents/salinopolis/dados/listas/';
lista_mes = dir([path_lista_mes, '*.txt']);
% stop

% leitura da lista de todos os arquivos HNE
% path_hne = '/home/hp/Documents/dados/pnboia/fortaleza/';
% pathfile_hne = importdata(['lista_hne.txt']);

% leitura dos dadoa de heave pitch e roll da boia
% path_hne = '/home/hp/Documents/salinopolis/dados/pnboia/HNE_fortaleza_201612/';
% a = dir([path_hne, '*.HNE']);

% leitura dos parametros meteo-oceaograficos da boia
param = readtable('/home/hp/Documents/dados/pnboia/pnboia_fortaleza.csv', 'HeaderLines', 0);

ws_boia = param.Wspd;
wd_boia = param.Wdir;

% vento do era5
wind_era5 = readtable('/home/hp/Documents/salinopolis/dados/era5/ERA5_param_fortaleza.csv', 'HeaderLines', 1);
ws_era5 = table2array(wind_era5(:,9));
wd_era5 = table2array(wind_era5(:,10));

% frequencia de amostragem
fs = 1.28;

% numero de pontos na fft (indica o graus de liberdade)
nfft = 240;

% arq1=[pathname_hne,arqp(ik,:),'.HNE'];
% disp([num2str(ik),' - ',num2str(arqp(ik,:))])
%eta, etaNS, etaEW

% path_out = '/home/hp/Documents/coppe/doutorado/output';

% parametros de onda e vento
% param = readtable([path_out, '/bmop_windwave_param.csv'], 'HeaderLines', 1);

% ws = param.Var16;
% wd = param.Var17;

% corrige o vento com o azimute medio


% leitura dos dados. pula 3 linhas para ficar com tamanho dos dados com media movel
% heave = readtable([path_out, '/bmop_wave_heave.csv'], 'HeaderLines', 1);
% pitch = readtable([path_out, '/bmop_wave_pitch.csv'], 'HeaderLines', 1);
% roll = readtable([path_out, '/bmop_wave_roll.csv'], 'HeaderLines', 1);

% bussola
% head = readtable([path_out, '/bmop_wave_head.csv'], 'HeaderLines', 1);
% [l,c]=size(head)

% azimute para tabela
% head1 = table2array(head(1,2:end));

% corrige direcao do vento com o azimute
% wd = wd + mean(head1, 2);


% data no formato de datetime
% datetime = datestr(datenum(heave.Var1, 'yyyy-mm-dd HH:MM:SS'));

%intervalo da amostragem (segund)
% fs = 1.28; %0.78;
% nfft = 240; %nfft=240 --> 16 gl

% mes = 05;
% ano = 2015;
% local = 'CF-01';

% %declinacao magnetica
% dmag = -23


% %carrega listas da axys
% % arq = load([pathname_hne,list_hne]);
% arqp = num2str(arq);

%vento
% time = load([pathname_cfsr, 'time_',file_cfsr]);
% u = load([pathname_cfsr, 'u',file_cfsr]);
% v = load([pathname_cfsr, 'v',file_cfsr]);

% wd(find(wd<0)) = wd(find(wd<0)) + 360;
% wd(find(wd>360)) = wd(find(wd>360)) - 360;

%inicia a contagem do tempo de processamento
% tic 

%% preparo dos arquivos

%cria matrizes de direcao, espec e energia com 10 linhas (representando 5
%faixas, cada uma com 2 direcoes; e 248 colunas representado o tempo (1 mes
%a cada 3 horas = 24/3*31)

% dire = zeros(10,length(arqp)); %direcao (2 valores, ate  5 faixas)
% espe = zeros(10,length(arqp)); %espectros (2 valores, ate 5 faixas)
% energ = zeros(10,length(arqp)); %Hm0 + 4 energias (uma por faixa), valor zero, 4 picos (maiores)
% dire1 = dire;
% espe1 = espe;

%vetor de frequencias (verificar se esta correto)
dt = 1 / fs; %intervalo de amostragem
fny = 1 / (2 * dt); %freq de nysquit
x = dt * nfft; %auxiliar para o vetor de freq (pq 64)
f1 = 1/x:1/x:fny; %vetor de freq - verificar com parente
df=f1(2) - f1(1); %deltaf

%picos1 é o valor da duracao da wavelet que será usada
%correspondendo a 3 ciclos do periodo de interesse

%quando nao ha pico na faixa:
% 48 -- 16s
% 27 -- 9s
% 18 -- 6s
% 9 -- 3s

picos1 = [48; 27; 18; 9];
% picos1 = [50; 25; 17; 8];

%entrada para daat
% co = n1;
% dd = n3;
% dc = n2;

%mesmo circulo mas agora com com 460 colunas
a26 = [a23(311:360) a23 a23(1:50)];
a27 = [a24(311:360) a24 a24(1:50)];

%cria vetor de 0 a 360, iniciando em 311 e terminando em 50
a30 = [(311:360) (1:360) (1:50)];

% ??
grad1 = 0.0175;
grad2 = 180/pi;

%para o caso de usar matr1 (matriz de ocorrencias)
sa = [.5;.5;.5;.5;0.1];

%cria vetor com o tamanho das wavelets
% mm sao as frequencies que podem conter pico no espectro
mm = [51;50;48;47;43;30;27;25;21;19;18;17;15;14;13;12;10;9];

% mm = round(1./f1);% mm = 100:-1:6;

ms = [];

%cria vetores de dim 64,34
wavecos = zeros(64,34);
wavesen = wavecos;

for i = 1:length(mm)
    
    mn = mm(i); %wavelet atual
    ms = [ms;mn];
    
    %cria vetoer de -pi a pi no tamanho de mn, que é o tamanho da wavelet
    out2 = linspace(-3.14,3.14,mn);
    
    %cria janela de hanning para o tamanho da wavelet
    gau = hanning(mn);
    
    %cria wavelet cos ??
    out1 = gau'.* cos(3 * out2);
    %cria wavelet sen ??
    out3 = gau'.* sin(3 * out2);
    
    %coloca em cada coluna a wavelet de determinado tamanho. cria 34
    %wavelets ??
    wavecos((1:mn)',i) = out1';
    wavesen((1:mn)',i) = out3';
end



% ================================================ %


% varia as listas de meses
for iim = 1:size(lista_mes)
    disp(lista_mes(iim).name)

    % leitura da lista dos arquivos HNE do mes
    paths_hne_mes = importdata([path_lista_mes, lista_mes(iim).name]);

    paths_hne_mes = sort(paths_hne_mes);

    if length(paths_hne_mes) >= 720
        disp(lista_mes(iim).name)

        kkl = 0;
        for ik = 1:length(paths_hne_mes)
            kkl = kkl + 1;
            disp (paths_hne_mes(ik))

            hne = dlmread(table2array(paths_hne_mes(ik)), '', 11, 0);
            n1 = hne(:,2);
            n2 = hne(:,4);
            n3 = hne(:,3);
            
            %calculo do espectro de 1 dimensao
            ww55 = zeros(8,1);

            [qq1 F]=pwelch(n1, hanning(nfft) ,nfft/2, nfft, fs);

            %correcao do fator de escala
            % qq1 = qq1(2:end,1);

            %coloca a altura significativa (hm0) na primeira linha de ww55)
            ww55(1) = 4 * sqrt(sum(qq1) * df);

            %cria faixas de freq (periodo)
            faixa1 = [10:18]; % 20.1 - 11.0 s
            faixa2 = [19:26]; % 10.4 - 7.5 s
            faixa3 = [27:38]; % 7.2 - 5.1 s
            faixa4 = [38:55]; % 4.9 - 3.2 s

            %espectros nas 4 faixas - 32 graus
            ww55(2) = sum(qq1(faixa1)); 
            ww55(3) = sum(qq1(faixa2)); 
            ww55(4) = sum(qq1(faixa3)); 
            ww55(5) = sum(qq1(faixa4)); 

            %picos calculados a partir de qq1        

            %calcula a diferença do vetor qq1 (ex qq1(2)-qq1(1)=g1(1) )
            g1 = diff(qq1);
            %coloca 1 para valores >1, 0 p/ =0 e -1 p/<0
            g1 = sign(g1);
            %calcula diferença (g1 ficou com 30 elementos)
            g1 = diff(g1);
            %deixa o vetor com 31 elementos
            g1 = [0;g1];
            %acha o indice do pico
            g1 = find(g1 == -2);

            %serao calculados os 4 maiores picos

            %acha os valores de energia dos picos (g4) e indices dos picos (g5)
            [g4 g5] = sort(qq1(g1));
            %coloca os indices em ordem crescente de energia
            g6 = flipud(g1(g5));
            %inicia criacao do vetor de picos (coloca zeros caso soh tiver 1 pico)
            g6 = [g6;0;0;0;0];
            %escolhe os 4 primeiros (maiores) picos
            g6 = g6(1:4);
            %retira valores maiores que 14 (para tirar picos na alta freq??)
            g7 = g6(g6<14);

            %colocacao dos picos nas primeiras faixas para determinacao das wavelets

            picos2 = zeros(4,1);

            for gh = 1:length(g7)

                %acha o indice da faixa1 que esta o valor g7(gh)
                g8 = find(g7(gh)==faixa1);
                
                %se não for matriz vazia, cria variavel logica: ans = 0 e
                %picos2(1) recebe o valor do pico, se nao nao faz nada
                isempty(g8);
                if ans == 0
                    picos2(1) = g7(gh);
                    faixa1 = 0;
                end
                    
                %acha o indice da faixa2 que esta o valor g7(gh)
                g8 = find(g7(gh)==faixa2);
                
                %se não for matriz vazia, cria variavel logica: ans = 0 e
                %picos2(2) recebe o valor do pico, se nao nao faz nada
                isempty(g8);
                if ans == 0
                    picos2(2) = g7(gh);
                    faixa2 = 0;
                end
                    
                %acha o indice da faixa3 que esta o valor g7(gh)
                g8 = find(g7(gh)==faixa3);
                
                %se não for matriz vazia, cria variavel logica: ans = 0 e
                %picos2(3) recebe o valor do pico, se nao nao faz nada
                isempty(g8);
                if ans == 0
                    picos2(3) = g7(gh);
                    faixa3 = 0;
                end      

                %acha o indice da faixa4 que esta o valor g7(gh)
                g8 = find(g7(gh)==faixa4);
                
                %se não for matriz vazia, cria variavel logica: ans = 0 e
                %picos2(4) recebe o valor do pico, se nao nao faz nada
                isempty(g8);
                if ans == 0
                    picos2(4) = g7(gh);
                    faixa4 = 0;
                end      
                    
            end

            %coloca o valor arredondado do pico * 3 em 'picos1'
            picos3 = picos1;    
            for gh = 1:4
                 if picos2(gh) > 0
                     picos1(gh) = round(3*1/f1(picos2(gh)));
                 end
            end

            %valores dos picos para o arquivo final
            g5 = flipud(g5); %indices dos picos em ordem decrescente
            g5 = g1(g5); %indices dos picos em ordem crescente
            g5 = [g5;0;0;0;0]; %coloca zeros caso nao tiver picos?
            g5 = g5(1:4); %acha os 4 maiores picos
            g = find(g5>0); %acha valores de picos maior que zero
            g5(g) = 64./g5(g); %acha os periodos dos picos em ordem crescente 
            % (pq divide por 64?)

            %coloca os 4 periodos de pico na linha 7 a 10 do ww55
            ww55(7:10) = g5;
            
            % o valor do vetor ww5 (10 linhas) contem:
            % ww55 = [hm0, sp1, sp2, sp3, sp4, 0 , tp1, tp2, tp3, tp4]
            % hm0 - altura significativa
            % sp - somatorio do vetor de energia por faixa
            % tp - periodo de pico de cada faixa

            %preparo final do energ

            %coloca o valor de ww55 na coluna kkl do energ
            energ(:,kkl) = ww55;

            %serao calculadas 5 faixas com wavelets
            %para cada wavelet calcula-se uma matriz de direcao e desvio
            %padrao obtendo-se um D(teta) para cada faixa

            %faixas variando de 1 a 4
            for iwq = 1:4

                %acha dentro de 'mm' o indice do valor de picos1(iwq)
                g11 = find(picos1(iwq) == mm);

                %acha o valor da wavelet
                m=mm(g11(1));

                %cria variavel out com a wavelet com o tamanho de 'm' a ser
                %utilizada (pega as linhas e coluna da wavelet)
                out1=wavecos((1:m)',g11(1));
                out3=wavesen((1:m)',g11(1));

                %cria matriz de 1
                matr1=ones(20,90);

                %perguntar para o parente
                m1=1024-m;

                %parametros para o calculo de tet2 e sp2
                m3=m1;
                m1=m1-1;
                m3=m1;
                %m4=2*dt/(m*0.375); comentado pois eh calculado dentro de 'daat1'
                m2=m-1;

                %chama subrotina 'daat1'
                daat1_ceara

                %dire1(iwq,kkl)=mean(tet2*180/pi);
                daat2_ceara
            end
        end

        % tempo_rodada = toc;

        % corrige a declinacao magnetica da onda
        % dire = dire + dmag

        % g = find(dire > 360);
        % dire(g) = dire(g) - 360;
        % g = find(dire > 360);
        % dire(g) = dire(g) - 360;

        % % corrige declinacao mag do vento
        % wd = wd + dmag

        % g = find(wd > 360);
        % wd(g) = wd(g) - 360;
        % g = find(wd > 360);
        % wd(g) = wd(g) - 360;

        %matriz de saida a cada 3 horas
        dire1 = dire(:,1:3:end); 
        espe1 = espe(:,1:3:end); 
        energ1 = energ(:,1:3:end);
        % azim1 = azim(1:3:end);

        % subtrai o aziumute da direcao
        % dire2 = bsxfun(@minus, dire1, azim1);

        ws1 = ws_boia(1:3:744);
        wd1 = wd_boia(1:3:744);

        % ws1 = ws_era5(1:3:744);
        % wd1 = wd_era5(1:3:744);

        filtradaat_bmop1
        dire1 = ddir;
        filtravento_bmop
        wd1 = wd2

        % a pleds entra com o dire1 e espe1 que sao os dados espacados a cada 3h
        pleds_ceara
    end
end