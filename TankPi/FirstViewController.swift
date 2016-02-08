//
//  FirstViewController.swift
//  TankPi
//
//  Created by Kevin McGill on 1/31/16.
//  Copyright © 2016 Kevin McGill. All rights reserved.
//

import UIKit

class FirstViewController: BaseViewController, HTTPsterDelegate {
    
    
    let imageUrl = NSURL(string: "https://tankpi.mcgilln.com/tank.jpg")
    let tempUrl = NSURL(string: "https://tankpi.mcgilln.com/temp.php")

    
    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet weak var label: UILabel!
    @IBOutlet weak var refresh: UIButton!
    

    override func viewDidLoad() {
        super.viewDidLoad()
        //Make delegate
        HTTPster.shared.delegate = self
        
        doRefresh()
    }

    
    
    @IBAction func refresh(sender: UIButton) {
        doRefresh()
    }
    
    func doRefresh() {
        //Get things
        HTTPster.shared.makeRequest(imageView, httpType: HTTPster.HTTPMethod.GET, contentType: nil, url: imageUrl!, headers: nil, postBody: nil)
        HTTPster.shared.makeRequest("temp", httpType: HTTPster.HTTPMethod.GET, contentType: nil, url: tempUrl!, headers: nil, postBody: nil)
    }
    
    func didRetrieveResponse(tag: Any, response: NSURLResponse?, responsedata: NSData?, error: NSError?) {
        
        if let image = tag as? UIImageView {
            if image == imageView {
                if let goodData = responsedata {
                    print("good image")
                    imageView.image = UIImage(data: goodData)
                }
            }
        }
        
        if let goodString = tag as? String {
            if goodString == "temp" {
                //Its the temp.
                if let goodData = responsedata {
                    let tempResponse = NSString(data: goodData, encoding: NSUTF8StringEncoding)
                    if let goodResponse = tempResponse as? String {
                        let tempIs = goodResponse.stringByTrimmingCharactersInSet(NSCharacterSet.whitespaceAndNewlineCharacterSet()) + " F"
                        print(tempIs)
                        label.text = tempIs
                    }
                    
                }
            }
        }
    }
}

