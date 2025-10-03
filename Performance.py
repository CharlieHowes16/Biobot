    elif game_state == "Performance_Page":
        main_pages_layout()
        text_line("PERFORMANCE", FONT, BLACK, 500, 10)

        red, amber, green = RAG_scores()
        text_line(f"Red: {red}", SMALL_FONT, RED, 300, 200)
        text_line(f"Amber: {amber}", SMALL_FONT, (255, 191, 0), 300, 250)
        text_line(f"Green: {green}", SMALL_FONT, DARK_GREEN, 300, 300)
