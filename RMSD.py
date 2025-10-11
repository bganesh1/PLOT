import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io

st.title("📈 RMSD Plotter with Unit Selection")

# --- Unit Selection ---
unit = st.selectbox("Select RMSD unit:", ["Å (Angstrom)", "nm (Nanometer)"])
scale_factor = 0.1 if unit == "nm (Nanometer)" else 1.0
y_label_unit = "nm" if unit == "nm (Nanometer)" else "Å"

# --- File Upload ---
uploaded_files = st.file_uploader(
    "📂 Upload one or more RMSD data files (txt or xvg)",
    type=["txt", "xvg"],
    accept_multiple_files=True
)

# --- Function to preprocess input file ---
def load_data(file):
    clean_lines = []
    for line in file.getvalue().decode("utf-8").splitlines():
        if line.startswith(("#", "@")):  # Skip comment/meta lines
            continue
        clean_lines.append(line)
    return np.loadtxt(clean_lines)

# --- Color and label palette ---
colors = ['red', 'green', 'blue', 'magenta', 'black', 'orange', 'purple']
labels = [f"Dataset {i+1}" for i in range(len(uploaded_files))]

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded!")

    plt.figure(figsize=(10, 6))

    for i, file in enumerate(uploaded_files):
        try:
            data = load_data(file)
            # Scale RMSD values according to user-selected unit
            time = data[:,0]
            rmsd = data[:,1] * scale_factor
            plt.plot(time, rmsd, linewidth=1.5, alpha=1.0, color=colors[i % len(colors)], label=labels[i])
        except Exception as e:
            st.warning(f"⚠️ Could not process {file.name}: {e}")

    # Customize plot appearance
    plt.xticks(np.arange(0, 251, 50), size=14, fontweight='bold')
    plt.yticks(size=14, fontweight='bold')
    plt.xlim(0, 251)

    # Bold axis labels
    plt.xlabel('Time ($\\mathbf{ns}$)', size=14, fontweight='bold')
    plt.ylabel(f'RMSD ($\\mathbf{{{y_label_unit}}}$)', size=14, fontweight='bold')

    # Customize legend
    leg = plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    for line in leg.get_lines():
        line.set_linewidth(4)
    for text in leg.get_texts():
        text.set_fontsize(14)
        text.set_fontweight('bold')

    # Bold ticks and spines
    ax = plt.gca()
    ax.tick_params(axis='both', which='major', labelsize=14, width=1.5, length=6, direction='in', labelcolor='black')
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)

    st.pyplot(plt)

    # --- Save figure to bytes buffer for download ---
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=1200, bbox_inches='tight')
    buf.seek(0)

    st.download_button(
        label="💾 Download RMSD Plot (PNG)",
        data=buf,
        file_name=f"RMSD_plot_{y_label_unit}.png",
        mime="image/png"
    )
else:
    st.info("📌 Upload RMSD files to see the plot.")
