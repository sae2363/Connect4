Authors:

Kyle Huang
and
Alfonso Arnal

Modify the agent tags in the MAIN file (select which agents you wish to play) and run the file.

pytest options

    To play on the CLI use this command 
        pytest test_run_cli.py -s
    
    You can also run the GUI via pytest with this command
        pytest main.py -s

If you want to run the code to get the data used in kyle's analysis, run the MTCS_graphs.py python file.  Once it finishes running a window will pop up with the results.  This can't be run with pytest yet. 

More detailed analysis is located in the txt files

Each analysis has some overlap but are better detailed on the section of the projects we worked on.

Notes:

Some code could have been better written but for time reasons and enviorment issues, extra files might exist.  

Alpha beta is allow unlimted time to run while MCTS is stuck in a range of 0.5 to 2 seconds so on boards larger then the real connect 4 game,  MCTS will lose it accuracy.

Contributions to major files:

    board.py Kyle
    
    MCTS.py Kyle
    
    Alphabeta.py Alfonso
    
    gui.py Alfonso
    
    cli.py Kyle
    
    main.py Alfonso
    
    MCTS_graphs Kyle
    
    Tests.py (ab data)  Alfonso
    
