//
//  FirstViewController.swift
//  TankPi
//
//  Created by Kevin McGill on 1/31/16.
//  Copyright © 2016 Kevin McGill. All rights reserved.
//

import UIKit

class FirstViewController: BaseViewController {
    
    
    let url = NSURL(string: "https://tankpi.mcgilln.com/")
    
    @IBOutlet weak var webview: UIWebView!
    @IBOutlet weak var refresh: UIButton!
    

    override func viewDidLoad() {
        super.viewDidLoad()
        doRefresh()
    }

    
    
    @IBAction func refresh(sender: UIButton) {
        doRefresh()
    }
    
    func doRefresh() {
        webview.loadRequest(NSURLRequest(URL: url!))
    }
    
}

