package main

import (
	"fmt"
	"os"
	"os/exec"
	"strings"
)

func main() {
	var result string
	fmt.Println("Welcome to BigCat installer")
	fmt.Print("Do you want to compile BigCat (Y/n) ")
	fmt.Scan(&result)

	if strings.ToLower(result) == "y" {
		err := install()
		if err != nil {
			fmt.Println("❌ Error during the installation:", err)
			return
		}
		fmt.Println("✅ BigCat was installed successfully :]")
	} else {
		fmt.Println("❌ BigCat was not installed")
	}
}

func install() error {

	cmd := exec.Command("bash", "-c",
		fmt.Sprintf("python3 -m PyInstaller --onefile bigcat.py"),
	)

	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	return cmd.Run()
}
