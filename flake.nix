{
    description = "SHB2-Superbot flake";
    inputs = {
        nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
        flake-utils.url = "github:numtide/flake-utils";
    };

    outputs = { self, nixpkgs, flake-utils }:
        flake-utils.lib.eachDefaultSystem ( system: 
            let
                pkgs = nixpkgs.legacyPackages.${system};
                lib = pkgs.lib;
            in {
                devShells.default = pkgs.mkShell {
                    buildInputs = with pkgs;
                        [ git docker ] ++ (with python311Packages; [
                        python
                    ]); 
                pure = true;
            };
      }
    );
}
