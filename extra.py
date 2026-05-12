def _show_date_in_sidebar(self):
         # 1. Display the date at the very top of the sidebar
                today_date = dt.now().strftime('%B %d, %Y')
    
                st.markdown(
                            f"""
                            <style>
                                .header-date {{
                                    position: fixed;
                                    top: 0.2rem;     /* Vertically centers in the header bar */
                                    right: 0.5rem;    /* Positions it to the left of the Deploy button */
                                    z-index: 1000000; /* Ensures it stays on top of Streamlit UI */
                                    color: #393a3b;
                                    font-size: 11px;
                                    font-weight: bold;
                                    font-family: sans-serif;
                                }}
                                /* Hide on mobile to prevent overlapping menu icons */
                                @media (max-width: 768px) {{
                                    .header-date {{ display: none; }}
                                }}
                            </style>
                    <div class="header-date">
                        Date: {today_date}
                    </div>
                    """
                            , unsafe_allow_html=True
                )