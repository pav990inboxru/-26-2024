#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Программа для создания таблиц покупок и продаж для игры Stay Out
Стиль оформления в стиле S.T.A.L.K.E.R.
Автор: Harper_IDS
Создано для игрового сообщества IgromanDS
"""

import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортируем и запускаем основное приложение
from stay_out_market_table_creator import main

if __name__ == "__main__":
    main()