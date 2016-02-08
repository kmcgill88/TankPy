//
//  FirstViewController.swift
//  TankPi
//
//  Created by Kevin McGill on 1/31/16.
//  Copyright © 2016 Kevin McGill. All rights reserved.
//

import UIKit

class FirstViewController: UIViewController, HTTPsterDelegate {
    
    
    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet weak var label: UILabel!
    @IBOutlet weak var refresh: UIButton!
    

    override func viewDidLoad() {
        super.viewDidLoad()
        //Make delegate
        HTTPster.shared.delegate = self
    }

    
    
    @IBAction func refresh(sender: UIButton) {
    
    
    }
    
    func didRetrieveResponse(tag: Any, response: NSURLResponse?, responsedata: NSData?, error: NSError?) {
        
    }

}

