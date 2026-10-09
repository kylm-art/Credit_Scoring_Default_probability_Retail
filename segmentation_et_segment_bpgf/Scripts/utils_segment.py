
import pandas as pd
from IPython.display import display, HTML
from itables import show

import matplotlib.pyplot as plt
import seaborn as sns


# Thème sombre façon VS Code / pandas : fond noir, texte blanc
_CSS = """
<style>
/* ---------- Fond sombre forcé sur tout le conteneur DataTables ---------- */
.dt-container,
.dt-container .dt-layout-row,
.dt-container .dt-layout-cell,
.dt-container .dt-scroll,
.dt-container .dt-scroll-head,
.dt-container .dt-scroll-headInner,
.dt-container .dt-scroll-body,
.dt-container .dt-scroll-foot {
    background:#181818 !important;
}
.dt-container { color:#e6e6e6 !important; padding:8px !important; border-radius:6px;
                font-family:Segoe UI, Roboto, Arial, sans-serif; }
.dt-container * { color:#e6e6e6; }
.dt-container .dt-search label, .dt-container .dt-length label,
.dt-container .dt-info { color:#e6e6e6 !important; }

/* ---------- Parents ajoutés par Jupyter / VS Code autour de la sortie ---------- */
div:has(> .dt-container), div:has(> div > .dt-container),
.output_html:has(.dt-container), .jp-RenderedHTMLCommon:has(.dt-container) {
    background:#181818 !important;
}

/* ---------- Tableau ---------- */
table.dataTable { font-size:13px; border-collapse:collapse !important; background:#181818 !important; }

/* En-tête : même fond que le tableau, texte blanc en gras */
table.dataTable thead th { background:#181818 !important; color:#ffffff !important;
                           font-weight:700; border-bottom:1px solid #3a3a3a !important; }
table.dataTable thead th * { color:#ffffff !important; }

/* Lignes alternées sombres, comme pandas */
table.dataTable tbody td { padding:6px 10px !important; border-bottom:none !important; }
table.dataTable tbody tr:nth-child(odd)  > * { background:#1f1f1f !important; box-shadow:none !important; }
table.dataTable tbody tr:nth-child(even) > * { background:#181818 !important; box-shadow:none !important; }
table.dataTable tbody tr:hover > *          { background:#2d3a4a !important; }

/* Titre (paramètre titre=) */
table.dataTable caption { caption-side:top; text-align:left; font-weight:700;
                          font-size:15px; padding:4px 0 8px 0; color:#ffffff !important; }

/* ---------- Recherche, sélecteur de lignes, boutons, pagination ---------- */
.dt-container .dt-search input, .dt-container .dt-length select {
    background:#1f1f1f !important; color:#e6e6e6 !important; border:1px solid #555 !important; }
.dt-container .dt-button {
    background:#2a2a2a !important; color:#e6e6e6 !important; border:1px solid #555 !important; }
.dt-container .dt-button:hover { background:#3a3a3a !important; }
.dt-container .dt-paging .dt-paging-button { color:#e6e6e6 !important; }
.dt-container .dt-paging .dt-paging-button.current,
.dt-container .dt-paging .dt-paging-button:hover {
    background:#3a3a3a !important; color:#ffffff !important; border:1px solid #555 !important; }
.dt-container .dt-paging .dt-paging-button.disabled { color:#666 !important; }

/* Menu déroulant "Column visibility" */
div.dt-button-collection { background:#1f1f1f !important; border:1px solid #555 !important; }
div.dt-button-collection .dt-button { background:#1f1f1f !important; }
div.dt-button-collection .dt-button.dt-button-active { background:#2d3a4a !important; }
</style>
"""


def afficher_tableau(df, titre=None, lignes=15, index=False, decimales=2,
             max_bytes=2 * 1024 * 1024, buttons=["colvis", "copy", "csv", "excel"],
               **kwargs):
    """
    Affiche un DataFrame sous forme de tableau interactif lisible.

    Paramètres
    ----------
    df        : DataFrame (ou Series) à afficher
    titre     : titre affiché au-dessus du tableau
    lignes    : nombre de lignes par page (modifiable ensuite dans le tableau)
    index     : afficher l'index pandas (utile pour value_counts, groupby...)
    decimales : arrondi des colonnes numériques
    max_bytes : taille max des données embarquées ; au-delà, itables sous-échantillonne.
                Mettre 0 pour tout afficher (attention aux très grosses bases).
    **kwargs  : toute autre option itables / DataTables (remplace les valeurs par défaut)
    """
    if isinstance(df, pd.Series):
        df = df.to_frame()
    d = df.copy()

    # Arrondi des nombres décimaux
    cols_float = d.select_dtypes(include="float").columns
    d[cols_float] = d[cols_float].round(decimales)

    # Alignement : nombres à droite, texte à gauche
    decalage = d.index.nlevels if index else 0
    pos_num = [i + decalage for i, c in enumerate(d.columns)
               if pd.api.types.is_numeric_dtype(d[c]) and not pd.api.types.is_bool_dtype(d[c])]

    options = dict(
        showIndex=index,
        paging=True,
        pageLength=lignes,
        lengthMenu=[[10, 15, 25, 50, 100, -1], [10, 15, 25, 50, 100, "Tout"]],
        scrollX=True,                 # défilement horizontal si beaucoup de colonnes
        ordering=True,                # tri en cliquant sur les en-têtes
        classes="display nowrap compact",
        maxBytes=max_bytes,
        layout={
            "topStart": ["pageLength", "buttons"],
            "topEnd": "search",
            "bottomStart": "info",
            "bottomEnd": "paging",
        },
        buttons=buttons,
        columnDefs=[
            {"className": "dt-right", "targets": pos_num},
            {"className": "dt-left", "targets": "_all"},
        ],
    )
    options.update(kwargs)

    display(HTML(_CSS))
    if titre:
        display(HTML(
            f"<div style='font-weight:700; font-size:15px; color:#ffffff; "
            f"background:#181818; padding:8px 8px 0 8px;'>{titre}</div>"
        ))
    show(d, **options)


def resume_variables(df):
    """Récapitulatif des variables : type, valeurs manquantes, valeurs distinctes."""
    nb_manq = df.isnull().sum()
    return pd.DataFrame({
        "Nom_Variable": df.columns,
        "Type_Donnée": df.dtypes.astype(str).values,
        "Nb_Valeurs_Manquantes": nb_manq.values,
        "%_Valeurs_Manquantes": (nb_manq / len(df) * 100).round(2).values,
        "Nb_Valeurs_Distinctes": df.nunique().values,
    })




def tableau_cible(df, var, cible="ddefaut_ndb", titre=None):
    """Tableau croisé var x cible : effectifs + % en ligne + poids de chaque modalité."""
    libelles = {0: "Non défaut", 1: "Défaut"}

    effectifs = pd.crosstab(df[var], df[cible], margins=True, margins_name="Total")
    pct = pd.crosstab(df[var], df[cible], normalize="index",
                      margins=True, margins_name="Total") * 100

    tableau = pd.concat(
        [effectifs.rename(columns=libelles),
         pct.rename(columns=libelles).add_suffix(" (%)")],
        axis=1,
    )
    tableau["Poids (%)"] = tableau["Total"] / len(df) * 100
    tableau = tableau.round(2).rename_axis(index=var, columns=None).reset_index()

    afficher_tableau(tableau, titre=titre or f"Répartition de {cible} par {var}",
             buttons=["colvis"])


def graphique_taux_defaut(df, var, cible="ddefaut_ndb", titre=None, rotation=15):
    """Barres du taux de défaut par modalité, étiquette « nb défauts (taux %) »."""
    stats = df.groupby(var, observed=True)[cible].agg(["sum", "mean"])
    stats["mean"] *= 100

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=stats.index.astype(str), y=stats["mean"],
                hue=stats.index.astype(str), palette="Reds_d", legend=False, ax=ax)

    for i, (n, t) in enumerate(zip(stats["sum"], stats["mean"])):
        ax.annotate(f"{int(n):,} ({t:.2f}%)".replace(",", " "), (i, t),
                    ha="center", va="bottom", fontsize=10, weight="bold",
                    xytext=(0, 3), textcoords="offset points")

    ax.set_title(titre or f"Taux de défaut ({cible}) par {var}", fontsize=13, weight="bold")
    ax.set_xlabel(var, fontsize=11)
    ax.set_ylabel("Taux de défaut (%)", fontsize=11)
    ax.tick_params(axis="x", rotation=rotation)
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    ax.set_axisbelow(True)
    ax.set_ylim(0, stats["mean"].max() * 1.15)
    plt.tight_layout()
    plt.show()