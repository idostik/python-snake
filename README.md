# Hra snake proti počítači

Hra je založená na klasické hře Snake, ale na hracím poli jsou hadi dva. Jednoho ovládá hráč a druhý je ovládaný počítačem. Cílem hráče je přežít déle než protivník.

### Ovládání
Po otevření hry uživatel hru spustí mezerníkem. Samotný had je ovládán pomocí šipek (hráč má defaultně modrou barvu a začíná v levém horním rohu). Hra lze ukončit pomocí klávesy Escape.

### Pravidla hry
Had se pravidelně jednou za daný časový interval pohne ve zvoleném směru. Pokud had narazí (sám do sebe, protivníka, nebo zdi), prohraje. Který had narazil do koho je vždy jasné, protože se hadi nehýbou ve stejný čas a nemůže tak nastat sporná kolize. Pokud had sebere jídlo, které se náhodně po jednom objevuje na hrací ploše, zvětší se. Pokud je jeden z hadů výrazně menší než druhý, tak prohraje.

### Requirements
Aby program správně fungoval, je potřeba mít nainstalovaných několik balíčků. Všechno potřebné je ve virtuálním prostředí *pyt_sem*, které můžete spustit příkazem ```conda activate pyt_sem``` (pokud nemáte nainstalovanou *Minicondu*, je potřeba ji nejprve nainstalovat). Při prvním spuštěním budete možná muset nejprve virtuální prostředí aktualizovat příkazem ```conda env update``` v adresáři *sem*.

### Spuštění hry
Po aktivování virtuálního prostředí hru spustíte z adresáře *sem* pomocí příkazu ```python3 snake_game```.

### Testování
Všechny testy můžete najednou spustit z adresáře *sem* pomocí příkazu ```pytest```.
