//
//  HTTPster.swift
//  CheeseBall
//
//  Created by Kevin on 11/1/14.
//  Copyright (c) 2014 Kevin McGill d/b/a McGill DevTech. All rights reserved.
//

import UIKit
import Foundation



public protocol HTTPsterDelegate {
    func didRetrieveResponse(tag:Any,response: NSURLResponse?, responsedata: NSData?, error: NSError?)
}


public class HTTPster : NSObject {
    
    public class var shared : HTTPster {
        struct Static {
            static let instance : HTTPster = HTTPster()
        }
        return Static.instance
    }
    
    public enum HTTPMethod:String {
        case POST = "POST"
        case GET = "GET"
    }
    
    public enum HTTPContentType:String {
        case URL_ENCODED = "application/x-www-form-urlencoded"
        case TEXT_HTML = "text/html"
        case TEXT_PLAIN = "text/plain"

    }

    public var delegate:HTTPsterDelegate?
    let HTTP_TIMEOUT = 15.0

    
    public func makeRequest(tag:Any, httpType:HTTPMethod, contentType:HTTPContentType?, url:NSURL, headers:[String:String]?, postBody: String?) {
        
        let request:NSMutableURLRequest = NSMutableURLRequest()
        request.URL = url
        request.HTTPMethod = httpType.rawValue
        request.timeoutInterval = HTTP_TIMEOUT
        
        if let type = contentType {
            request.setValue(type.rawValue, forHTTPHeaderField: "Content-Type")
        }
        
        
        if HTTPMethod.POST == httpType {
            if var goodBody = postBody {
                goodBody = goodBody.stringByAddingPercentEncodingWithAllowedCharacters(NSCharacterSet.URLQueryAllowedCharacterSet())!
                let bodyData = goodBody.dataUsingEncoding(NSASCIIStringEncoding, allowLossyConversion: true)!
                request.HTTPBody = bodyData
                request.setValue("\(bodyData.length)", forHTTPHeaderField: "Content-Length")
            }
        }

        //Set all Headers as needed
        if let theHeaders = headers {
            for (key, value) in theHeaders {
                request.setValue(value, forHTTPHeaderField: key)
            }
            
        }
        
        doCall(tag, request: request)
    }
    
    
    func doCall(tag:Any,request:NSMutableURLRequest) {
        
        let session = NSURLSession.sharedSession().dataTaskWithRequest(request, completionHandler: {(data: NSData?, response: NSURLResponse?, error: NSError?) in

            dispatch_async(dispatch_get_main_queue()){
                    self.delegate?.didRetrieveResponse(tag, response: response, responsedata: data, error: error)
            }
            
        })
        session.resume()
        
    }

}