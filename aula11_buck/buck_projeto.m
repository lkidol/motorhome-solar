%% buck_projeto.m - SEM0320 Aula 11: Buck 24 V -> 12 V
% Dimensionamento analitico + ensaios A (ideal), B (perdas didaticas) e
% C (componentes comerciais) com o modelo chaveado explicito do slide 44/45.
% Gera as figuras em ./fig/*.pdf (vetoriais) e imprime as tabelas no console.
%
% STATUS: nao foi executado no MATLAB (so verificado em Python equivalente,
% buck_check.py). Rode em uma sessao limpa e confira os numeros contra o relatorio.
clear; clc; close all;
if ~exist('fig','dir'), mkdir fig; end

%% ---------------- Parametros (unico lugar) ----------------
Vin = 24;  Vo_ref = 12;  fs = 20e3;  Ts = 1/fs;     % V, V, Hz, s
R1 = 12;   R2 = 6;                                  % ohm: antes / depois do degrau
t_end = 100e-3;  t_step = 50e-3;                    % s
dIL_max = 0.40;  dvo_max = 0.12;                    % A pp, V pp
L = 1e-3;  C = 100e-6;                              % H, F (valores comerciais escolhidos)

% struct: rS (RDS_on), rL (DCR), rC (ESR), VF
par.A = struct('rS',0,    'rL',0,     'rC',0,     'VF',0    );  % ideal
par.B = struct('rS',0.050,'rL',0.100, 'rC',0.100, 'VF',0.500);  % parasitas didaticos (slide 46)
par.C = struct('rS',0.020,'rL',0.195, 'rC',0.130, 'VF',0.525);  % componentes escolhidos (conferir datasheet)

%% ---------------- Etapa 1: dimensionamento ----------------
D0     = Vo_ref/Vin;
L_min  = (Vin-Vo_ref)*D0/(fs*dIL_max);              % ondulacao de corrente
L_crit = (1-D0)*R1/(2*fs);                          % fronteira CCM/DCM em R = 12 ohm
rC_d   = par.C.rC;
C_min  = dIL_max/(8*fs*(dvo_max - rC_d*dIL_max));   % regra do slide 36 (soma conservadora)
fprintf('D=%.3f | L_min=%.0f uH | L_crit(12 ohm)=%.0f uH | C_min=%.1f uF (rC=%.0f mOhm)\n', ...
    D0, L_min*1e6, L_crit*1e6, C_min*1e6, rC_d*1e3);
dIL = (Vin-Vo_ref)*D0/(L*fs);
fprintf('L=%.0f uH, C=%.0f uF: dIL=%.3f A, ILmin(12 ohm)=%.3f A, ILpk(2 A)=%.3f A, ILrms=%.4f A\n', ...
    L*1e6, C*1e6, dIL, 1-dIL/2, 2+dIL/2, sqrt(4+dIL^2/12));

%% ---------------- D com perdas (slide 45) e simulacoes ----------------
Dfun = @(p,Io) (Vo_ref + p.VF + Io*p.rL)/(Vin + p.VF - Io*p.rS);
D.A = 0.5;  D.B = Dfun(par.B, 2);  D.C = Dfun(par.C, 2);
fprintf('D_A=%.4f | D_B=%.4f | D_C=%.4f\n', D.A, D.B, D.C);

cases = {'A','B','C'};
res = struct();
for k = 1:numel(cases)
    c = cases{k};
    res.(c) = simula_buck(par.(c), D.(c), L, C, Vin, Ts, t_end, t_step, R1, R2);
end

%% ---------------- Metricas (janelas 30-40 ms e 90-100 ms) ----------------
fprintf('\n%-4s %-8s %8s %9s %8s %8s %8s %8s %7s\n', 'caso','carga','vo_med','dvo_pp','diL_pp','iLmin','Pin','Pout','eta');
for k = 1:numel(cases)
    c = cases{k};
    for j = 1:2
        if j==1, w=[30e-3 40e-3]; Rn='12 ohm'; else, w=[90e-3 100e-3]; Rn='6 ohm'; end
        m = metricas(res.(c), w, Ts, Vin);
        fprintf('%-4s %-8s %8.4f %9.5f %8.4f %8.4f %8.3f %8.3f %6.2f%%\n', ...
            c, Rn, m.vo_med, m.dvo_pp, m.diL_pp, m.iL_min, m.Pin, m.Pout, 100*m.eta);
    end
    % transitorio de degrau e partida
    s = res.(c);  v6 = metricas(s,[90e-3 100e-3],Ts,Vin).vo_med;
    post = s.t >= t_step;  tp = s.t(post);  vp = s.vo(post);
    idx = find(abs(vp - v6) > 0.01*v6, 1, 'last');
    if isempty(idx), t_acom = 0; else, t_acom = tp(idx) - t_step; end
    fprintf('   %s: degrau: vo_min=%.3f V (desvio %.3f V), acomodacao(1%%)=%.2f ms, iL_max=%.3f A | partida: iL_max=%.3f A, vo_max=%.3f V\n', ...
        c, min(vp), min(vp)-v6, t_acom*1e3, max(s.iL(post)), max(s.iL(s.t<20e-3)), max(s.vo(s.t<20e-3)));
end

%% ---------------- Perdas estimadas a 2 A (caso C, slide 29) ----------------
Io = 2;  p = par.C;
RDS = p.rS;  Qg = 63e-9;  Vgs = 12;  Qgd = 23e-9;      % TODO: conferir no datasheet do IRFZ44N
tr = 60e-9;  tf = 45e-9;                                 % TODO: conferir (AUIRFZ44N: VDD=28 V, ID=25 A, RG=12 ohm)
Irms2  = Io^2 + dIL^2/12;
P_cond = RDS*D.C*Irms2;
P_diod = p.VF*(1-D.C)*Io;
P_ind  = p.rL*Irms2;
P_esr  = p.rC*dIL^2/12;
P_drv  = Qg*Vgs*fs;
P_sw_a = 0.5*Vin*Io*(tr+tf)*fs;                          % tr/tf do datasheet
P_sw_b = 0.5*Vin*Io*(Qgd/0.130 + Qgd/0.270)*fs;          % limitado pelo IR2104 (130/270 mA)
Pout = Vo_ref*Io;
for P_sw = [P_sw_a P_sw_b]
    Pl = P_cond+P_diod+P_ind+P_esr+P_drv+P_sw;
    fprintf('Perdas: cond=%.3f diodo=%.3f L=%.3f ESR=%.4f sw=%.3f drv=%.3f | total=%.3f W | eta=%.2f%%\n', ...
        P_cond,P_diod,P_ind,P_esr,P_sw,P_drv,Pl,100*Pout/(Pout+Pl));
end

%% ---------------- Figuras (geradas do MATLAB) ----------------
% 1) Regime permanente: ultimos 10 periodos de cada janela, casos A e C
for c = {'A','C'}
    cc = c{1};  s = res.(cc);
    f = figure('Position',[100 100 900 700]);
    for j = 1:2
        if j==1, w=[40e-3-10*Ts 40e-3]; Rn='12'; else, w=[100e-3-10*Ts 100e-3]; Rn='6'; end
        m = s.t>=w(1) & s.t<=w(2);
        subplot(2,2,j);      plot((s.t(m)-w(1))*1e3, s.iL(m),'LineWidth',1.2); grid on;
        xlabel('t - t_0 (ms)'); ylabel('i_L (A)'); title(sprintf('Caso %s, R = %s \\Omega',cc,Rn));
        subplot(2,2,j+2);    plot((s.t(m)-w(1))*1e3, s.vo(m),'LineWidth',1.2); grid on;
        xlabel('t - t_0 (ms)'); ylabel('v_o (V)');
    end
    exportgraphics(f, sprintf('fig/regime_%s.pdf',cc), 'ContentType','vector');
end
% 2) Degrau de carga (janela 45-60 ms), A vs C
f = figure('Position',[100 100 900 650]);
for k = [1 3]
    s = res.(cases{k});  m = s.t>=45e-3 & s.t<=60e-3;
    subplot(2,1,1); plot(s.t(m)*1e3, s.vo(m),'LineWidth',1.1,'DisplayName',['Caso ' cases{k}]); hold on;
    subplot(2,1,2); plot(s.t(m)*1e3, s.iL(m),'LineWidth',1.1,'DisplayName',['Caso ' cases{k}]); hold on;
end
subplot(2,1,1); grid on; ylabel('v_o (V)'); legend('Location','best'); title('Degrau de carga 12 \Omega \rightarrow 6 \Omega em 50 ms');
subplot(2,1,2); grid on; ylabel('i_L (A)'); xlabel('t (ms)'); legend('Location','best');
exportgraphics(f,'fig/degrau.pdf','ContentType','vector');
% 3) Partida (0-20 ms), A vs C
f = figure('Position',[100 100 900 650]);
for k = [1 3]
    s = res.(cases{k});  m = s.t<=20e-3;
    subplot(2,1,1); plot(s.t(m)*1e3, s.vo(m),'LineWidth',1.1,'DisplayName',['Caso ' cases{k}]); hold on;
    subplot(2,1,2); plot(s.t(m)*1e3, s.iL(m),'LineWidth',1.1,'DisplayName',['Caso ' cases{k}]); hold on;
end
subplot(2,1,1); grid on; ylabel('v_o (V)'); legend('Location','best'); title('Partida com D constante, R = 12 \Omega');
subplot(2,1,2); grid on; ylabel('i_L (A)'); xlabel('t (ms)'); legend('Location','best');
exportgraphics(f,'fig/partida.pdf','ContentType','vector');

%% ================= funcoes locais =================
function s = simula_buck(p, D, L, C, Vin, Ts, t_end, t_step, R1, R2)
% Modelo chaveado explicito (slides 44-45). Estados: iL, vC. Integra por
% segmento (chave ligada / desligada) com ode23tb e evento iL = 0 (DCM).
    opts = odeset('RelTol',1e-6,'AbsTol',1e-9,'MaxStep',Ts/100);
    t = 0;  x = [0; 0];                                  % iL(0)=0, vC(0)=0
    T = []; X = []; Q = [];
    for k = 0:round(t_end/Ts)-1
        if k*Ts < t_step, R = R1; else, R = R2; end      % degrau alinhado ao inicio de um periodo
        for q = [1 0]
            if q == 1, dur = D*Ts; else, dur = (1-D)*Ts; end
            t1 = t + dur;
            f   = @(~,x) dinamica(x, q, p, L, C, Vin, R);
            if q == 0, o = odeset(opts,'Events',@evento_iL_zero); else, o = opts; end
            [tt, xx, te] = ode23tb(f, [t t1], x, o);
            if q == 0 && ~isempty(te)                    % DCM: iL=0 ate o proximo periodo
                xz = xx(end,:).';  xz(1) = 0;
                g  = @(~,y) [0; (-(y(2)/(1+p.rC/R))/R)/C];
                [t2, x2] = ode23tb(g, [te t1], xz, opts);
                tt = [tt; t2(2:end)];  xx = [xx; x2(2:end,:)];
            end
            T = [T; tt];  X = [X; xx];  Q = [Q; q*ones(size(tt))];
            t = t1;  x = xx(end,:).';
        end
    end
    s.t = T;  s.iL = X(:,1);  s.vC = X(:,2);  s.q = Q;
    Rv = R1*(T < t_step) + R2*(T >= t_step);
    s.R = Rv;
    s.vo = (s.vC + p.rC*s.iL)./(1 + p.rC./Rv);
end

function [value, isterminal, direction] = evento_iL_zero(~, x)
    value = x(1);  isterminal = 1;  direction = -1;      % iL cruza zero decrescendo
end

function dx = dinamica(x, q, p, L, C, Vin, R)
    iL = x(1);  vC = x(2);
    vo = (vC + p.rC*iL)/(1 + p.rC/R);
    if q == 1
        diL = (Vin - p.rS*iL - p.rL*iL - vo)/L;
    else
        if iL > 0, diL = (-p.VF - p.rL*iL - vo)/L; else, diL = 0; end
    end
    dx = [diL; (iL - vo/R)/C];
end

function m = metricas(s, w, Ts, Vin)
% Medias na janela w (numero inteiro de periodos); ondulacao nos ultimos 10 periodos.
    k  = s.t >= w(1) & s.t <= w(2);
    t  = s.t(k);  T = t(end) - t(1);
    m.vo_med = trapz(t, s.vo(k))/T;
    m.Pin    = trapz(t, Vin*s.q(k).*s.iL(k))/T;
    m.Pout   = trapz(t, s.vo(k).^2./s.R(k))/T;
    m.eta    = m.Pout/m.Pin;
    l = k & s.t >= w(2) - 10*Ts;
    m.dvo_pp = max(s.vo(l)) - min(s.vo(l));
    m.diL_pp = max(s.iL(l)) - min(s.iL(l));
    m.iL_min = min(s.iL(l));
end
