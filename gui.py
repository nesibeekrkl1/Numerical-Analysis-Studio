import numpy as np
import matplotlib.pyplot as plt
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importing the mathematical engine from main.py
from main import SayisalAnalizMotoru  # Note: If you rename the class inside main.py, update this line.

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class NumericalAnalysisApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Numerical Analysis Studio")
        self.geometry("950x600")
        self.resizable(True, True)

        # Main Layout Configuration
        self.grid_columnconfigure(0, weight=4, minsize=380)
        self.grid_columnconfigure(1, weight=6, minsize=500)
        self.grid_rowconfigure(0, weight=1)

        # ------------------------------------------
        # LEFT INPUT PANEL
        # ------------------------------------------
        self.left_panel = ctk.CTkFrame(self, corner_radius=15, fg_color="#1e1e24")
        self.left_panel.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        
        self.lbl_title = ctk.CTkLabel(self.left_panel, text="MATHEMATICAL INPUTS", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_title.pack(pady=(20, 15))

        # Function Input Card
        self.frame_func = ctk.CTkFrame(self.left_panel, fg_color="#2a2a35", corner_radius=10)
        self.frame_func.pack(pady=6, padx=20, fill="x")
        self.lbl_func = ctk.CTkLabel(self.frame_func, text="Function f(x):", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_func.pack(anchor="w", padx=15, pady=(8, 2))
        self.txt_func = ctk.CTkEntry(self.frame_func, placeholder_text="E.g., x**2 - sin(x) - 4", height=35)
        self.txt_func.pack(fill="x", padx=15, pady=(0, 10))

        # Analysis Point Card
        self.frame_x = ctk.CTkFrame(self.left_panel, fg_color="#2a2a35", corner_radius=10)
        self.frame_x.pack(pady=6, padx=20, fill="x")
        self.lbl_x = ctk.CTkLabel(self.frame_x, text="Analysis Point (x):", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_x.pack(anchor="w", padx=15, pady=(8, 2))
        self.txt_x = ctk.CTkEntry(self.frame_x, placeholder_text="2.0", height=35)
        self.txt_x.pack(fill="x", padx=15, pady=(0, 10))

        # Integration Limits Card
        self.frame_integral = ctk.CTkFrame(self.left_panel, fg_color="#2a2a35", corner_radius=10)
        self.frame_integral.pack(pady=6, padx=20, fill="x")
        self.lbl_integral = ctk.CTkLabel(self.frame_integral, text="Integration Limits [a, b]:", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_integral.pack(anchor="w", padx=15, pady=(8, 2))
        
        self.sub_frame_int = ctk.CTkFrame(self.frame_integral, fg_color="transparent")
        self.sub_frame_int.pack(fill="x", padx=15, pady=(0, 10))
        self.txt_lower = ctk.CTkEntry(self.sub_frame_int, placeholder_text="Lower (a)", height=35)
        self.txt_lower.pack(side="left", expand=True, fill="x", padx=(0, 5))
        self.txt_upper = ctk.CTkEntry(self.sub_frame_int, placeholder_text="Upper (b)", height=35)
        self.txt_upper.pack(side="left", expand=True, fill="x", padx=(5, 0))

        # Calculate Button
        self.btn_calculate = ctk.CTkButton(
            self.left_panel, text="ANALYZE AND UPDATE PLOT", 
            font=ctk.CTkFont(size=12, weight="bold"), fg_color="#1f6aa5",
            hover_color="#144871", height=45, corner_radius=10, command=self.calculate
        )
        self.btn_calculate.pack(pady=(20, 15), padx=20, fill="x")

        # ------------------------------------------
        # RIGHT REPORT AND PLOT PANEL
        # ------------------------------------------
        self.right_panel = ctk.CTkFrame(self, corner_radius=15, fg_color="#14141a")
        self.right_panel.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        self.lbl_report_title = ctk.CTkLabel(self.right_panel, text="ANALYSIS REPORT AND VISUALIZATION", font=ctk.CTkFont(size=14, weight="bold"), text_color="#a0a0a5")
        self.lbl_report_title.pack(pady=(15, 5))

        # Report Textbox
        self.txt_report = ctk.CTkTextbox(self.right_panel, font=ctk.CTkFont(family="Consolas", size=12), fg_color="#1c1c24", border_color="#2b2b36", border_width=1, corner_radius=10, height=160)
        self.txt_report.pack(fill="x", padx=20, pady=(0, 10))
        
        # Plot Frame
        self.plot_frame = ctk.CTkFrame(self.right_panel, fg_color="#1c1c24", corner_radius=10)
        self.plot_frame.pack(expand=True, fill="both", padx=20, pady=(0, 15))
        
        # Matplotlib Integration
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(expand=True, fill="both", padx=5, pady=5)
        
        self.apply_plot_style()
        self.canvas.draw()
        self.display_message("System ready.\nEnter the values in the left panel and click 'ANALYZE'.")

    def calculate(self):
        func_text = self.txt_func.get().strip()
        if not func_text:
            self.display_message("[!] ERROR: Please enter a function to analyze.")
            return

        try:
            x_point = float(self.txt_x.get()) if self.txt_x.get() else 0.0
            lower_limit = float(self.txt_lower.get()) if self.txt_lower.get() else 0.0
            upper_limit = float(self.txt_upper.get()) if self.txt_upper.get() else 0.0

            # Calculations are done via main.py (SayisalAnalizMotoru)
            f_result = SayisalAnalizMotoru.f(x_point, func_text)
            derivative_result = SayisalAnalizMotoru.sayisal_turev(x_point, func_text)
            integral_result = SayisalAnalizMotoru.trapez_integral(lower_limit, upper_limit, func_text)
            root_result = SayisalAnalizMotoru.kok_bul_bisection(func_text)

            report_text = (
                f" CALCULATION COMPLETED SUCCESSFULLY\n"
                f" ------------------------------------------------------------\n"
                f" Equation: f(x) = {func_text}\n"
                f" ------------------------------------------------------------\n"
                f"  • f({x_point}) Value        : {f_result:.5f}\n"
                f"  • f'({x_point}) Derivative   : {derivative_result:.5f}\n"
                f"  • [{lower_limit}, {upper_limit}] Integral  : {integral_result:.5f}\n"
                f"  • Approx. Root (Bisection): {root_result}\n"
                f" ------------------------------------------------------------"
            )
            self.display_message(report_text)
            self.update_plot(func_text)

        except Exception as e:
            self.display_message(f"[!] ERROR OCCURRED\n\nPlease check your inputs or function syntax.\n\nDetails: {e}")

    def display_message(self, text):
        self.txt_report.configure(state="normal")
        self.txt_report.delete("1.0", "end")
        self.txt_report.insert("1.0", text)
        self.txt_report.configure(state="disabled")

    def apply_plot_style(self):
        """Sets the background color and axis styles for the plot."""
        self.fig.patch.set_facecolor('#1c1c24')
        self.ax.set_facecolor('#242430')
        self.ax.tick_params(colors='#a0a0a5', labelsize=9)
        self.ax.grid(True, color='#3a3a4a', linestyle=':', linewidth=0.5)
        for spine in self.ax.spines.values():
            spine.set_color('#4a4a5a')

    def update_plot(self, func_text):
        self.ax.clear()
        self.apply_plot_style()
        
        x_axis = np.linspace(-10, 10, 500)
        y_axis = []

        for val in x_axis:
            try:
                res = SayisalAnalizMotoru.f(val, func_text)
                if isinstance(res, (int, float, np.number)):
                    y_axis.append(float(res))
                else:
                    y_axis.append(np.nan)
            except:
                y_axis.append(np.nan)

        self.ax.plot(x_axis, y_axis, color="#1f6aa5", linewidth=2, label="f(x)")
        self.ax.axhline(0, color='white', linewidth=0.6, linestyle='--')
        self.ax.axvline(0, color='white', linewidth=0.6, linestyle='--')
        self.ax.legend(facecolor='#1c1c24', edgecolor='#4a4a5a', labelcolor='white', fontsize=9)
        
        self.canvas.draw()

if __name__ == "__main__":
    app = NumericalAnalysisApp()
    app.mainloop()