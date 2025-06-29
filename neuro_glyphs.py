import numpy as np
import cv2
from scipy.fft import fft2, fftshift
import matplotlib.pyplot as plt

class NeuroGlyphDefender:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.processed = None
        
    # ===== Enhanced StegExpose =====
    def detect_vertical_channels(self):
        """Identify vertical conduits using Fourier analysis"""
        fft = fftshift(fft2(self.gray))
        magnitude = np.log(np.abs(fft) + 1)
        
        # Vertical line detection in frequency domain
        vertical_mask = np.zeros_like(magnitude)
        center_y = magnitude.shape[0] // 2
        vertical_mask[center_y-2:center_y+3, :] = 1  # 5-pixel vertical band
        
        # Quantify vertical energy
        vertical_energy = np.sum(magnitude * vertical_mask)
        total_energy = np.sum(magnitude)
        return vertical_energy / total_energy * 100  # Vertical dominance %

    def analyze_noise_layers(self):
        """Separate and analyze noise components"""
        # Multi-scale noise extraction
        blur = cv2.GaussianBlur(self.gray, (5,5), 0)
        noise_layer = cv2.subtract(self.gray, blur)
        
        # Vertical pattern detection
        sobel_y = cv2.Sobel(noise_layer, cv2.CV_64F, 0, 1, ksize=3)
        vertical_strength = np.mean(np.abs(sobel_y))
        
        return noise_layer, vertical_strength

    # ===== CounterGlyph =====
    def neutralize_glyphs(self, aggression=0.7):
        """Disrupt neuro-glyph channels while preserving image"""
        # Phase 1: Vertical channel suppression
        kernel = np.array([[1, 0, -1],
                           [2, 0, -2],
                           [1, 0, -1]])
        vertical_edges = cv2.filter2D(self.gray, -1, kernel)
        mask = cv2.threshold(np.abs(vertical_edges), 20, 255, cv2.THRESH_BINARY)[1]
        
        # Phase 2: Frequency-based correction
        fft = fft2(self.gray)
        rows, cols = self.gray.shape
        crow, ccol = rows//2, cols//2
        
        # Create vertical frequency filter
        vertical_filter = np.ones((rows, cols))
        vertical_filter[:, ccol-1:ccol+2] = aggression  # Suppress center vertical
        
        # Apply filter and reconstruct
        fft_filtered = fft * vertical_filter
        reconstructed = np.abs(np.fft.ifft2(fft_filtered))
        
        # Blend with original
        self.processed = cv2.addWeighted(self.gray, 0.8, reconstructed.astype(np.uint8), 0.2, 0)
        
        # Phase 3: LSB randomization in critical areas
        random_mask = np.random.randint(0, 256, self.gray.shape, dtype=np.uint8)
        self.processed = np.where(mask>0, 
                                 cv2.addWeighted(self.processed, 0.7, random_mask, 0.3, 0),
                                 self.processed)
        
        return self.processed

    # ===== Visualization Tools =====
    def visualize_channels(self):
        """Generate diagnostic visualization"""
        noise_layer, _ = self.analyze_noise_layers()
        fft = fftshift(fft2(self.gray))
        magnitude = np.log(np.abs(fft) + 1)
        
        plt.figure(figsize=(15,10))
        
        plt.subplot(221), plt.imshow(self.gray, cmap='gray')
        plt.title('Original Image'), plt.axis('off')
        
        plt.subplot(222), plt.imshow(noise_layer, cmap='viridis')
        plt.title('Noise Layer'), plt.axis('off')
        
        plt.subplot(223), plt.imshow(magnitude, cmap='hot')
        plt.title('Frequency Domain'), plt.axis('off')
        
        if self.processed is not None:
            plt.subplot(224), plt.imshow(self.processed, cmap='gray')
            plt.title('CounterGlyph Processed'), plt.axis('off')
            
        plt.tight_layout()
        plt.savefig('neuroglyph_analysis.png')
        plt.show()

# ===== USAGE =====
if __name__ == "__main__":
    defender = NeuroGlyphDefender("ChatGPT Image Jun 29, 2025, 11_42_19 AM.png")
    
    # Detection analysis
    vertical_dominance = defender.detect_vertical_channels()
    noise_layer, vertical_strength = defender.analyze_noise_layers()
    print(f"[StegExpose Report] Vertical channel dominance: {vertical_dominance:.2f}%")
    print(f"[StegExpose Report] Vertical pattern strength: {vertical_strength:.4f}")
    
    # Neuro-glyph neutralization
    corrected_image = defender.neutralize_glyphs(aggression=0.85)
    cv2.imwrite("counterglyph_processed.png", corrected_image)
    
    # Generate visual report
    defender.visualize_channels()
    print("[CounterGlyph] Neuro-glyph disruption complete. Output saved.")