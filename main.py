import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
from tkinter import Tk, filedialog
import datetime

# --- Abrir seletor de arquivo ---
Tk().withdraw()
caminho = filedialog.askopenfilename(
    title="Selecione uma imagem",
    filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")]
)

if not caminho:
    print("❌ Nenhuma imagem foi selecionada.")
    exit()

# --- Carregar a imagem selecionada ---
imagem = cv2.imread(caminho, cv2.IMREAD_GRAYSCALE)
if imagem is None:
    print("❌ Erro ao carregar a imagem.")
    exit()

# --- Transformada de Fourier ---
f = np.fft.fft2(imagem)
fshift_original = np.fft.fftshift(f)
linhas, colunas = imagem.shape
centro = (linhas // 2, colunas // 2)

# --- Espectro de Fourier ---
magnitude_spectrum = 20 * np.log(np.abs(fshift_original) + 1)

# --- Função para aplicar máscara circular/coroa ---
def aplicar_coroa(fshift, r_in, r_out, modo_bloqueio=True):
    Y, X = np.ogrid[:linhas, :colunas]
    dist = np.sqrt((X - centro[1])**2 + (Y - centro[0])**2)
    if modo_bloqueio:
        mascara = (dist < r_in) | (dist > r_out)
    else:
        mascara = (dist >= r_in) & (dist <= r_out)
    fshift_mascarado = fshift * mascara
    f_ishift = np.fft.ifftshift(fshift_mascarado)
    img_rec = np.fft.ifft2(f_ishift)
    return np.abs(img_rec)

# --- Inicialização da interface ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 6))
plt.subplots_adjust(left=0.1, bottom=0.35)

# Exibir imagens iniciais
ax1.imshow(imagem, cmap='gray')
ax1.set_title("Imagem Original")
ax1.axis('off')

modificada = aplicar_coroa(fshift_original, 0, min(centro), modo_bloqueio=True)
img2 = ax2.imshow(modificada, cmap='gray')
ax2.set_title("Imagem Pós-Transformada")
ax2.axis('off')

ax3.imshow(magnitude_spectrum, cmap='gray')
ax3.set_title("Espectro de Fourier")
ax3.axis('off')

# --- Sliders ---
r_max = min(centro)
ax_raio_in = plt.axes([0.2, 0.22, 0.6, 0.03])
ax_raio_out = plt.axes([0.2, 0.17, 0.6, 0.03])
slider_in = Slider(ax_raio_in, 'Raio Interno', 0, r_max - 1, valinit=0, valstep=1)
slider_out = Slider(ax_raio_out, 'Raio Externo', 1, r_max, valinit=r_max, valstep=1)

# --- Botão de salvar ---
ax_save = plt.axes([0.15, 0.05, 0.2, 0.06])
btn_save = Button(ax_save, 'Salvar imagem')

# --- Checkbox para alternar modo ---
ax_check = plt.axes([0.5, 0.05, 0.3, 0.12])
check = CheckButtons(ax_check, ['Modo bloqueio (remove coroa)'], [True])
modo_bloqueio = [True]  # precisa estar numa lista para ser mutável

# --- Overlay de coroa no espectro ---
patches = []

def desenhar_overlay(r_in, r_out):
    # Limpa patches antigos
    global patches
    for p in patches:
        p.remove()
    patches = []

    # Cria dois círculos: raio interno e externo
    circ_in = Circle((centro[1], centro[0]), r_in)
    circ_out = Circle((centro[1], centro[0]), r_out)

    # Criar uma máscara para o anel entre r_in e r_out
    # Usaremos um PatchCollection para preencher área entre os dois círculos

    # Para preencher o anel, desenhamos o círculo externo preenchido, e o interno preenchido com branco para "recortar"
    # Mas matplotlib não suporta diretamente "buracos", então faremos com transparência e ordem

    # Primeiro, círculo externo preenchido vermelho semitransparente
    pc_out = PatchCollection([circ_out], facecolor='red', alpha=0.3, edgecolor=None)
    ax3.add_collection(pc_out)
    patches.append(pc_out)

    # Segundo, círculo interno preenchido branco para esconder o centro (simula o buraco)
    pc_in = PatchCollection([circ_in], facecolor='white', alpha=1.0, edgecolor=None)
    ax3.add_collection(pc_in)
    patches.append(pc_in)

    fig.canvas.draw_idle()

# --- Função de atualização ---
def atualizar(val):
    r_in = slider_in.val
    r_out = slider_out.val
    if r_in >= r_out:
        return
    nova_img = aplicar_coroa(fshift_original, r_in, r_out, modo_bloqueio=modo_bloqueio[0])
    img2.set_data(nova_img)
    desenhar_overlay(r_in, r_out)
    fig.canvas.draw_idle()

# --- Função do botão salvar ---
def salvar(event):
    r_in = slider_in.val
    r_out = slider_out.val
    img_final = aplicar_coroa(fshift_original, r_in, r_out, modo_bloqueio[0])
    nome_arquivo = f"imagem_filtrada_{r_in:.0f}_{r_out:.0f}_{datetime.datetime.now().strftime('%H%M%S')}.png"
    cv2.imwrite(nome_arquivo, img_final)
    print(f"✅ Imagem salva como {nome_arquivo}")

# --- Alternar modo ---
def alternar_modo(label):
    modo_bloqueio[0] = not modo_bloqueio[0]
    atualizar(None)

# --- Conectar eventos ---
slider_in.on_changed(atualizar)
slider_out.on_changed(atualizar)
btn_save.on_clicked(salvar)
check.on_clicked(alternar_modo)

# --- Inicializa overlay ---
desenhar_overlay(slider_in.val, slider_out.val)

plt.show()
